import uuid
from uuid import UUID
from functools import partial
from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List, Type, Optional, Union

from app.dao.base_dao import BaseDAO
from app.dao.address_dao import AddressDAO
from app.dao.role_dao import RoleDAO
from app.utils import DAOResponse, Hash
from app.models import User, Addresses, Role
from app.schema import UserResponse, Address, AddressBase, UserAuthInfo, UserUpdateSchema, UserCreateSchema, UserEmergencyInfo, UserBase, UserAuthCreateInfo, UserEmployerInfo

class UserDAO(BaseDAO[User]):
    def __init__(self, model: Type[User],load_parent_relationships: bool = False, load_child_relationships: bool = False, excludes = []):
        super().__init__(model, load_parent_relationships, load_child_relationships, excludes=excludes)
        self.primary_key = "user_id"
        self.address_dao = AddressDAO(Addresses)

    @override
    async def create(self, db_session: AsyncSession, obj_in: Union[UserCreateSchema | Dict]) -> DAOResponse[UserResponse]:
        try:
            user_data = obj_in
            
            # check if user exists
            existing_user : User = await self._user_exists(db_session, user_data.get('email'))
            if existing_user:
                return DAOResponse[UserResponse](success=False, error="User already exists", data=UserResponse.from_orm_model(existing_user))

            # extract base information
            user_info = self.extract_model_data(user_data, UserBase)

            # create new user
            new_user: User = await super().create(db_session=db_session, obj_in=user_info)
            user_id = new_user.user_id

            # create verification token and password hash
            if 'user_auth_info' in user_data and user_data['user_auth_info'] and 'password' in  user_data['user_auth_info']:
                user_data['user_auth_info']['password'] = Hash.bcrypt(user_data['user_auth_info']['password'])
                user_data['user_auth_info']['verification_token'] = str(uuid.uuid4())
                user_data['user_auth_info']['is_subscribed_token'] = str(uuid.uuid4())

            # add additional info if exists | Determine the correct schema for the address
            address_schema = Address if 'address' in user_data and user_data['address'] and 'address_id' in user_data['address'] else AddressBase
            details_methods = {
                'user_emergency_info': (self.add_emergency_info, UserEmergencyInfo),
                'user_employer_info': (self.add_employment_info, UserEmployerInfo),
                'user_auth_info': (self.add_auth_info, UserAuthCreateInfo),
                'address': (partial(self.address_dao.add_entity_address, entity_model=self.model.__name__), address_schema)
            }

            if set(details_methods.keys()).issubset(set(user_data.keys())):
                await self.process_entity_details(db_session, user_id, user_data, details_methods)

            # check if role is attached and create role for user
            if 'role' in user_data.keys():
                await self.add_user_role(db_session, user_id, user_data.get('role'))

            user_load_addr: User = await self.query(
                db_session=db_session,
                filters={f"{self.primary_key}":user_id},
                single=True,
                options=[selectinload(User.addresses)]
            )
            
            # commit object to db session
            await self.commit_and_refresh(db_session, user_load_addr)
            return DAOResponse[UserResponse](success=True, data=UserResponse.from_orm_model(user_load_addr))
        
        except ValidationError as e:
            return DAOResponse(success=False, data=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[UserResponse](success=False, error=f"Fatal {str(e)}")
    
    @override
    async def update(self, db_session: AsyncSession, db_obj: User, obj_in: UserUpdateSchema) -> DAOResponse[UserResponse]:
        try:
            # get the entity dump info
            entity_data = obj_in.model_dump()

            # update user info
            existing_user : User = await super().update(db_session=db_session, db_obj=db_obj, obj_in=obj_in)
            user_id = existing_user.user_id

            # add additional info if exists | Determine the correct schema for the address
            address_schema = Address if 'address' in obj_in.model_fields and entity_data['address'] and 'address_id' in entity_data['address'] else AddressBase

            details_methods = {
                'user_emergency_info': (self.add_emergency_info, UserEmergencyInfo),
                'user_employer_info': (self.add_employment_info, UserEmployerInfo),
                'user_auth_info': (self.add_auth_info, UserAuthInfo),
                'address': (partial(self.address_dao.add_entity_address, entity_model=self.model.__name__), address_schema)
            }

            # add additional info if exists
            if set(details_methods.keys()).issubset(set(entity_data.keys())):
                await self.process_entity_details(db_session, user_id, entity_data, details_methods)
            
            # commit object to db session
            await self.commit_and_refresh(db_session, existing_user)
            return DAOResponse[UserResponse](success=True, data=UserResponse.from_orm_model(existing_user))

        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[UserResponse](success=False, error=f"Fatal Update {str(e)}")
    
    @override
    async def get_all(self, db_session: AsyncSession) -> DAOResponse[List[UserResponse]]:
        result = await super().get_all(db_session=db_session)
        
        # check if no result
        if not result:
            return DAOResponse(success=True, data=[])

        return DAOResponse[List[UserResponse]](success=True, data=[UserResponse.from_orm_model(r) for r in result])
    
    @override
    async def get(self, db_session: AsyncSession, id: Union[UUID | Any | int]) -> DAOResponse[UserResponse]:

        result = await super().get(db_session=db_session, id=id)

        # check if no result
        if not result:
            return DAOResponse(success=True, data={})

        return DAOResponse[UserResponse](success=True, data=UserResponse.from_orm_model(result))
 
    async def _user_exists(self, db_session: AsyncSession, email: str) -> bool:
        existing_user : User = await self.query(db_session=db_session, filters={"email": email}, single=True)
        return existing_user
    
    async def add_user_role(self, db_session: AsyncSession, user_id: str, role_alias: str):
        role_dao = RoleDAO(Role)

        try:
            async with db_session as db:
                user: User = await self.query(db_session=db, filters={f"{self.primary_key}": user_id},single=True,options=[selectinload(User.roles)])
                role: Role = await role_dao.query(db_session=db, filters={"alias": role_alias}, single=True)

                if user is None or role is None:
                    raise NoResultFound()
        
                if role in user.roles:
                    return DAOResponse[dict](success=False, error="Role already exists for the user", data=UserResponse.from_orm_model(user))
                
                user.roles.append(role)
                await self.commit_and_refresh(db, user)

                return DAOResponse[UserResponse](success=True, data=UserResponse.from_orm_model(user))
        except NoResultFound as e:
            return None
        except Exception as e:
            return DAOResponse[User](success=False, error=str(e))
        
    async def add_employment_info(self, db_session: AsyncSession, user_id: str, employee_info: UserEmployerInfo) -> Optional[User]:
        try:
            user : User = await self.query(db_session=db_session, filters={f"{self.primary_key}": user_id}, single=True)
            updated_user : User = await super().update(db_session=db_session, db_obj=user, obj_in=employee_info)

            return updated_user
        except NoResultFound:
            pass

    async def add_emergency_info(self, db_session: AsyncSession, user_id: str,  emergency_info: UserEmergencyInfo) -> Optional[User]:
        try:
            user : User = await self.query(db_session=db_session, filters={f"{self.primary_key}": user_id}, single=True)
            updated_user : User = await super().update(db_session=db_session, db_obj=user, obj_in=emergency_info)

            return updated_user
        except NoResultFound:
            pass

    async def add_auth_info(self, db_session: AsyncSession, user_id: str,  auth_info: UserAuthInfo) -> Optional[User]:
        try:
            user : User = await self.query(db_session=db_session, filters={f"{self.primary_key}": user_id}, single=True)
            updated_user : User = await super().update(db_session=db_session, db_obj=user, obj_in=auth_info)

            return updated_user
        except NoResultFound:
            pass