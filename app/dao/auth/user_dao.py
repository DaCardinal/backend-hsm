import uuid
import asyncio
from uuid import UUID
from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List, Optional, Union

# models
from app.models.user import User
from app.models.role import Role

# services
from app.services.email_service import EmailService

# utils
from app.utils.hashing import Hash
from app.utils.response import DAOResponse

# daos
from app.dao.auth.role_dao import RoleDAO
from app.dao.resources.base_dao import BaseDAO
from app.dao.address.address_dao import AddressDAO
from app.dao.contracts.rental_history_dao import PastRentalHistoryDAO

# schemas
from app.schema.enums import GenderEnum
from app.schema.user import (
    UserResponse,
    UserAuthInfo,
    UserUpdateSchema,
    UserCreateSchema,
    UserEmergencyInfo,
    UserBase,
    UserEmployerInfo,
)
from app.schema.mixins.user_mixins import PastRentalHistory, PastRentalHistoryBase

VERIFICATION_LINK = (
    "https://backend-hsm.onrender.com/auth/verify-email?email={}&token={}"
)
UNSUBSCRIBE_LINK = (
    "https://backend-hsm.onrender.com/auth/mail-unsubscribe?email={}&token={}"
)
# ACCOUNT_CREATION_LINK = "https://backend-hsm.onrender.com/update-account?token={}&email={}&first_name={}"


class UserDAO(BaseDAO[User]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = User
        self.primary_key = "user_id"

        self.address_dao = AddressDAO()
        self.role_dao = RoleDAO()
        self.rental_history_dao = PastRentalHistoryDAO()

        self.detail_mappings = {
            "user_auth_info": self.add_auth_info,
            "user_employer_info": self.add_employment_info,
            "user_emergency_info": self.add_emergency_info,
            "address": self.address_dao.add_entity_address,
            "rental_history": self.add_rental_history_info,
        }

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    @override
    async def create(
        self, db_session: AsyncSession, obj_in: Union[UserCreateSchema | Dict]
    ) -> DAOResponse[UserResponse]:
        try:
            user_data = obj_in

            # check if user exists
            existing_user: User = await self.user_exists(
                db_session, user_data.get("email")
            )

            if existing_user:
                raise Exception("User already exists")

            # prepare and create new user
            user_data["gender"] = GenderEnum(user_data["gender"])
            user_info = self.extract_model_data(user_data, UserBase)
            new_user: User = await super().create(
                db_session=db_session, obj_in=user_info
            )

            # verification and prepared
            verification_token, is_subscribed_token = (
                str(uuid.uuid4()),
                str(uuid.uuid4()),
            )
            self.prepare_auth_info(user_data, verification_token, is_subscribed_token)

            # process any entity details
            await self.handle_entity_details(
                db_session=db_session,
                entity_data=user_data,
                detail_mappings=self.detail_mappings,
                entity_model=self.model.__name__,
                entity_assoc_id=new_user.user_id,
            )

            # check if role is attached and create role for user
            if "role" in user_data.keys():
                await self.add_user_role(
                    db_session, new_user.user_id, user_data.get("role")
                )

            # update and refresh_user
            user_load_addr = await self.update_and_refresh_user(
                db_session, new_user, verification_token, is_subscribed_token
            )

            # send email to user
            await self.send_verification_email(
                new_user, verification_token, is_subscribed_token
            )

            return DAOResponse[UserResponse](
                success=True, data=[UserResponse.from_orm_model(user_load_addr)]
            )

        except ValidationError as e:
            return DAOResponse(success=False, data=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[UserResponse](success=False, error=f"Fatal {str(e)}")

    @override
    async def update(
        self, db_session: AsyncSession, db_obj: User, obj_in: UserUpdateSchema
    ) -> DAOResponse[UserResponse]:
        try:
            # get the entity dump info
            entity_data = obj_in.model_dump()

            # update user info
            existing_user: User = await super().update(
                db_session=db_session,
                db_obj=db_obj,
                obj_in=obj_in.model_dump(exclude=["user_id"]).items(),
            )
            user_id = existing_user.user_id

            # process any entity details
            await self.handle_entity_details(
                db_session=db_session,
                entity_data=entity_data,
                detail_mappings=self.detail_mappings,
                entity_model=self.model.__name__,
                entity_assoc_id=user_id,
            )

            # check if role is attached and create role for user
            if "role" in entity_data.keys():
                await self.add_user_role(db_session, user_id, entity_data.get("role"))

            return DAOResponse[UserResponse](
                success=True, data=UserResponse.from_orm_model(existing_user)
            )
        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except NoResultFound as e:
            return DAOResponse(success=False, error=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[UserResponse](
                success=False, error=f"Fatal Update {str(e)}"
            )

    @override
    async def get_all(
        self, db_session: AsyncSession, offset=0, limit=100
    ) -> DAOResponse[List[UserResponse]]:
        result = await super().get_all(
            db_session=db_session, offset=offset, limit=limit
        )

        return DAOResponse[List[UserResponse]](
            success=True, data=[UserResponse.from_orm_model(r) for r in result]
        )

    @override
    async def get(
        self, db_session: AsyncSession, id: Union[UUID | Any | int]
    ) -> DAOResponse[UserResponse]:
        result = await super().get(db_session=db_session, id=id)

        return DAOResponse[UserResponse](
            success=bool(result),
            data={} if result is None else UserResponse.from_orm_model(result),
        )

    def prepare_auth_info(
        self,
        user_data: Dict[str, Any],
        verification_token: str,
        is_subscribed_token: str,
    ):
        """
        Prepares the authentication information, including hashing the password and setting tokens.
        """
        if "user_auth_info" in user_data and user_data["user_auth_info"]:
            user_auth_info = user_data["user_auth_info"]

            if "password" in user_auth_info:
                user_auth_info["password"] = Hash.bcrypt(user_auth_info["password"])

            user_auth_info["verification_token"] = verification_token
            user_auth_info["is_subscribed_token"] = is_subscribed_token

    async def user_exists(self, db_session: AsyncSession, email: str):
        return await self.query(
            db_session=db_session, filters={"email": email}, single=True
        )

    async def get_user_and_role(
        self, db_session: AsyncSession, user_id: str, role_alias: str
    ) -> tuple[User, Role]:
        """
        Helper method to fetch the user and role based on their IDs.
        """
        user = await self.query(
            db_session=db_session,
            filters={f"{self.primary_key}": user_id},
            single=True,
            options=[selectinload(User.roles)],
        )
        role = await self.role_dao.query(
            db_session=db_session, filters={"alias": role_alias}, single=True
        )

        if user is None or role is None:
            raise NoResultFound("User or Role does not exist!")

        return user, role

    async def add_user_role(
        self, db_session: AsyncSession, user_id: str, role_alias: str
    ):
        try:
            user, role = await self.get_user_and_role(db_session, user_id, role_alias)

            if role in user.roles:
                return DAOResponse(
                    success=False, error="Role already exists for the user"
                )

            user.roles.clear()
            user.roles.append(role)

            await self.commit_and_refresh(db_session, user)

            return DAOResponse[UserResponse](
                success=True, data=UserResponse.from_orm_model(user)
            )
        except NoResultFound:
            return DAOResponse(success=False, error="User or role does not exist!")
        except Exception as e:
            return DAOResponse[User](success=False, error=str(e))

    async def remove_user_role(
        self, db_session: AsyncSession, user_id: str, role_alias: str
    ):
        try:
            user, role = await self.get_user_and_role(db_session, user_id, role_alias)

            if role not in user.roles:
                return DAOResponse(
                    success=False, error="Role doesn't exist for the user"
                )

            # TODO (DQ): Clear only a specified role
            user.roles.clear()
            await self.commit_and_refresh(db_session, user)

            return DAOResponse(success=True, data=UserResponse.from_orm_model(user))

        except NoResultFound:
            return DAOResponse(success=False, error="User or role does not exist!")
        except Exception as e:
            return DAOResponse[User](success=False, error=str(e))

    async def send_verification_email(
        self, user: User, verification_token: str, is_subscribed_token: str
    ):
        """
        Sends a verification email to the user.
        """
        email_service = EmailService()
        asyncio.create_task(
            email_service.send_user_email(
                user.email,
                f"{user.first_name} {user.last_name}",
                VERIFICATION_LINK.format(user.email, verification_token),
                UNSUBSCRIBE_LINK.format(user.email, is_subscribed_token),
            )
        )

    async def update_and_refresh_user(
        self,
        db_session: AsyncSession,
        user: User,
        verification_token: str,
        is_subscribed_token: str,
    ):
        """
        Updates the user's verification and subscription tokens and refreshes the session.
        """
        user_load_addr: User = await self.query(
            db_session=db_session,
            filters={f"{self.primary_key}": user.user_id},
            single=True,
            options=[selectinload(User.addresses)],
        )
        user.verification_token = verification_token
        user.is_subscribed_token = is_subscribed_token

        return await self.commit_and_refresh(db_session=db_session, obj=user_load_addr)

    async def add_employment_info(
        self, db_session: AsyncSession, user_id: str, employee_info: UserEmployerInfo
    ) -> Optional[User]:
        """
        Add or update employment information for a user.
        """
        return await self.add_user_detail(db_session, user_id, employee_info)

    async def add_emergency_info(
        self, db_session: AsyncSession, user_id: str, emergency_info: UserEmergencyInfo
    ) -> Optional[User]:
        """
        Add or update emergency contact information for a user.
        """
        # TODO: Add support for adding emergency address

        # 1. Create emergency_address hash if none passed
        if not emergency_info.emergency_address_hash:
            emergency_info.emergency_address_hash = str(uuid.uuid4())

        # 2. Create address
        # 3. Create entity_address object with entity_id as emergency_address
        # 4. Set emergency_address field on entity_address to True
        detail_mappings = {
            "address": self.address_dao.add_entity_address,
        }

        # process any entity details
        await self.handle_entity_details(
            db_session=db_session,
            entity_data=emergency_info.model_dump(),
            detail_mappings=detail_mappings,
            entity_model=self.model.__name__,
            entity_assoc_id=emergency_info.emergency_address_hash,
        )

        return await self.add_user_detail(db_session, user_id, emergency_info)

    async def add_auth_info(
        self, db_session: AsyncSession, user_id: str, auth_info: UserAuthInfo
    ) -> Optional[User]:
        """
        Add or update authentication information for a user.
        """
        return await self.add_user_detail(db_session, user_id, auth_info)

    async def add_rental_history_info(
        self,
        db_session: AsyncSession,
        entity_id: UUID,
        rental_history_info: Union[PastRentalHistory | List[PastRentalHistory]],
    ) -> Optional[List[PastRentalHistoryBase | PastRentalHistory]]:
        """
        Add or update rental history information for a user.
        """

        try:
            results = []
            rental_history_info = (
                rental_history_info
                if isinstance(rental_history_info, list)
                else [rental_history_info]
            )

            for rental_history in rental_history_info:
                # 1. create address hash if none passed
                if not rental_history.address_hash:
                    rental_history.address_hash = str(uuid.uuid4())

                # 2. assign user id
                rental_history.user_id = entity_id

                results.append(
                    await self.rental_history_dao.add_entity_rental_history(
                        db_session=db_session,
                        entity_id=entity_id,
                        rental_history_info=rental_history,
                    )
                )

            return results
        except Exception as e:
            return DAOResponse(success=False, error=f"Fatal {str(e)}")

    async def add_user_detail(
        self,
        db_session: AsyncSession,
        user_id: str,
        detail_info: Union[UserEmployerInfo | UserEmergencyInfo | UserAuthInfo],
    ) -> Optional[User]:
        """
        Generalized method to add or update user details.
        """
        try:
            user = await self.query(
                db_session=db_session,
                filters={f"{self.primary_key}": user_id},
                single=True,
            )
            return await super().update(
                db_session=db_session, db_obj=user, obj_in=detail_info
            )
        except NoResultFound:
            raise Exception("User does not exist!")
