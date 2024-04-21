from uuid import UUID
from pydantic import ValidationError
import pydantic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import selectinload
from typing import Type, Optional, Union, override

from app.dao.base_dao import BaseDAO
from app.dao.address_dao import AddressDAO
from app.dao.entity_dao import EntityDAO
from app.dao.role_dao import RoleDAO
from app.models.entity_address import EntityAddress
from app.utils.response import DAOResponse
from app.models import User, Addresses, Role
from app.schema.schemas import AddressCreateSchema, UserAuthInfo, UserCreateSchema, UserEmergencyInfo, UserBase, UserEmployerInfo

class UserDAO(BaseDAO[User]):
    def __init__(self, model: Type[User]):
        super().__init__(model)
        self.primary_key = "user_id"

    @override
    async def create(self, db_session: AsyncSession, obj_in: UserCreateSchema) -> Optional[User]:
        return await self.add_new_user(db_session, obj_in)
    
    async def add_new_user(self, db_session: AsyncSession, user_data: Union[UserCreateSchema, dict]) -> DAOResponse:
        try:
            # check if user exists
            existing_user : User = await self.user_exists(db_session, user_data.get('email'))
            if existing_user:
                return DAOResponse(success=False, error="User already exists")

            user_info = self.extract_data(user_data, UserBase)

            # create new user
            new_user: User = await super().create(db_session=db_session, obj_in=user_info)
            user_id = new_user.user_id

            # add additional info if exists
            await self.handle_user_details(db_session, user_id, user_data)
            user_load_addr: User = await self.query(
                db_session=db_session,
                filters={f"{self.primary_key}":user_id},
                single=True,
                options=[selectinload(User.addresses)]
            )
            
            # commit object to db session
            await self.commit_and_refresh(db_session, user_load_addr)
            return DAOResponse(success=True, data=new_user.to_dict())
        
        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[User](success=False, error=f"Fatal {str(e)}")
    
    async def user_exists(self, db_session: AsyncSession, email: str) -> bool:
        existing_user : User = await self.query(db_session=db_session, filters={"email": email}, single=True)
        return existing_user

    async def handle_user_details(self, db_session: AsyncSession, user_id: UUID, user_data: dict):
        details_methods = {
            'user_emergency_info': (self.add_emergency_info, UserEmergencyInfo),
            'user_employer_info': (self.add_employment_info, UserEmployerInfo),
            'user_auth_info': (self.add_auth_info, UserAuthInfo),
            'address': (self.add_user_address, AddressCreateSchema)
        }

        results = {}
        
        for detail_key, (method, schema) in details_methods.items():
            detail_data = self.extract_data(user_data, schema, nested_key=detail_key)
            
            if detail_data is not None:
                results[detail_key] = await method(db_session, user_id, schema(**detail_data))
        return results
    
    def extract_data(self, data: dict, schema: Type[pydantic.BaseModel], nested_key: Optional[str] = None) -> dict:
        if nested_key:
            data = data.get(nested_key, {})

        return {key: data[key] for key in data if key in schema.model_fields} if data else None
    
    async def add_user_role(self, db_session: AsyncSession, user_id: str, role_alias: str):
        role_dao = RoleDAO(Role)

        try:
            async with db_session as db:
                user: User = await self.query(db_session=db, filters={f"{self.primary_key}": user_id},single=True,options=[selectinload(User.roles)])
                role: Role = await role_dao.query(db_session=db, filters={"alias": role_alias}, single=True)

                if user is None or role is None:
                    raise NoResultFound()
        
                if role in user.roles:
                    return DAOResponse[dict](success=False, error="Role already exists for the user", data=user.to_dict())
                
                user.roles.append(role)
                await self.commit_and_refresh(db, user)

                return DAOResponse[dict](success=True, data=user.to_dict())
        except NoResultFound as e:
            return DAOResponse[dict](success=False, error="User or Role not found")
        except Exception as e:
            return DAOResponse[User](success=False, error=str(e))
        
    async def add_employment_info(self, db_session: AsyncSession, user_id: str, employee_info: UserEmployerInfo) -> Optional[User]:
        try:
            user : User = await self.query(db_session=db_session, filters={f"{self.primary_key}": user_id}, single=True)
            updated_user : User = await self.update(db_session=db_session, db_obj=user, obj_in=employee_info.model_dump())

            return updated_user
        except NoResultFound:
            pass

    async def add_emergency_info(self, db_session: AsyncSession, user_id: str,  emergency_info: UserEmergencyInfo) -> Optional[User]:
        try:
            user : User = await self.query(db_session=db_session, filters={f"{self.primary_key}": user_id}, single=True)
            updated_user : User = await self.update(db_session=db_session, db_obj=user, obj_in=emergency_info.model_dump())

            return updated_user
        except NoResultFound:
            pass

    async def add_auth_info(self, db_session: AsyncSession, user_id: str,  auth_info: UserAuthInfo) -> Optional[User]:
        try:
            user : User = await self.query(db_session=db_session, filters={f"{self.primary_key}": user_id}, single=True)
            updated_user : User = await self.update(db_session=db_session, db_obj=user, obj_in=auth_info.model_dump())

            return updated_user
        except NoResultFound:
            pass

    async def add_user_address(self, db_session: AsyncSession, entity_id: UUID, address_obj: AddressCreateSchema) -> Optional[Addresses]:
        address_dao = AddressDAO(Addresses)
        entity_address_dao = EntityDAO(EntityAddress)

        try:
            # Create a new Address instance from the validated address_data
            new_address : Addresses = await address_dao.create(db_session=db_session, address_data=address_obj)
            
            # Link user model to new addresses
            entity_address = await entity_address_dao.create(db_session = db_session, obj_in = {
                "entity_type": self.model.__name__,
                "entity_id": entity_id,
                "address_id": new_address.address_id,
                "emergency_address": False,
                "emergency_address_hash": ""
            })
            return entity_address
        
        except Exception as e:
            return DAOResponse[dict](success=False, error=f"An unexpected error occurred {e}")