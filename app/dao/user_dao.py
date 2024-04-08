from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from typing import Type, Optional, Union, override

from app.dao.base_dao import BaseDAO
from app.dao.address_dao import AddressDAO
from app.dao.entity_dao import EntityDAO
from app.dao.role_dao import RoleDAO
from app.utils.response import DAOResponse
from app.models import User, Addresses, Role
from app.schema.schemas import AddressCreateSchema, UserCreateSchema, UserEmergencyInfo, UserBase, UserEmployerInfo

class UserDAO(BaseDAO[User]):
    def __init__(self, model: Type[User]):
        super().__init__(model)
        self.primary_key = "user_id"
    
    @override
    async def create(self, db_session: AsyncSession, obj_in: UserCreateSchema):
        return await self.add_new_user(db_session=db_session, user_data=obj_in)
    
    async def add_new_user(self, db_session: AsyncSession, user_data: Union[UserCreateSchema, dict]) -> Optional[User]:
        try:
            user_base_info_data = {key: user_data[key] for key in user_data if key in UserBase.model_fields}
            emergency_info_data = {key: user_data[key] for key in user_data if key in UserEmergencyInfo.model_fields}
            employment_info_data = {key: user_data[key] for key in user_data if key in UserEmployerInfo.model_fields}

            # check if user exists
            existing_user = await self.query(db_session=db_session, filters={"email": user_data.get('email')}, single=True)

            if existing_user:
                return DAOResponse[User](success=False, error="User already exists")  
            
            # Create a new User instance
            new_user: User = await super().create(db_session=db_session, obj_in=user_base_info_data)

            # Add employment info, if present
            if employment_info_data:
                try:
                    validated_employment_info = UserEmployerInfo(**employment_info_data)
                    new_user = await self.add_employment_info(db_session=db_session, user_id=new_user.user_id, employee_info=validated_employment_info)
                except ValidationError as e:
                    return DAOResponse[User](success=False, validation_error=e)

            # Add emergency info
            if emergency_info_data:
                try:
                    validated_emergency_info = UserEmergencyInfo(**emergency_info_data)
                    new_user: User = await self.add_emergency_info(db_session=db_session, user_id=new_user.user_id, emergency_info = validated_emergency_info)
                except ValidationError as e:
                    return DAOResponse[User](success=False, validation_error=e)
            
            # TODO: Change DAO response to parse object corectly
            return DAOResponse[dict](success=True, data=new_user.to_dict())
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[User](success=False, error=f"An unexpected error occurred {e}")

    async def add_user_role(self, db_session: AsyncSession, user_id: str, role_alias: str) -> Optional[User]:
        role_dao = RoleDAO()

        try:
            user : User = await self.query(db_session=db_session, filters={f"{self.primary_key}": user_id}, single=True)
            role : Role = await role_dao.query(db_session=db_session, filters={"alias": role_alias}, single=True)

            # attach role to user
            user.roles.append(role)

            return user
        except NoResultFound:
            pass

    async def add_employment_info(self, db_session: AsyncSession, user_id: str, employee_info: UserEmployerInfo) -> Optional[User]:
        try:
            user : User = await self.query(db_session=db_session, filters={f"{self.primary_key}": user_id}, single=True)
            updated_user : User = await self.update(db_session=db_session, db_obj=user, obj_in=employee_info)

            return updated_user
        except NoResultFound:
            pass

    async def add_emergency_info(self, db_session: AsyncSession, user_id: str,  emergency_info: UserEmergencyInfo) -> Optional[User]:
        try:
            user : User = await self.query(db_session=db_session, filters={f"{self.primary_key}": user_id}, single=True)
            updated_user : User = await self.update(db_session=db_session, db_obj=user, obj_in=emergency_info)

            return updated_user
        except NoResultFound:
            pass

    async def add_user_address(self, db_session: AsyncSession, user_id: str, address_obj: AddressCreateSchema) -> Optional[User]:
        address = AddressDAO()
        entity_address = EntityDAO()

        try:
            user = await self.query(db_session=db_session, filters={f"{self.primary_key}": user_id}, single=True)
            
            # Create a new Address instance from the validated address_data
            new_address : Addresses = address.create(address_obj)
            
            # Link user model to new addresses
            entity_address.create(db_session = db_session, obj_in = {
                "entity_type": "User",
                "entity_id": user_id,
                "address_id": new_address.address_id
            })

            return user
        
        except NoResultFound:
            return None