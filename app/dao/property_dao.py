from functools import partial
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Type, Union, override

from app.dao.base_dao import BaseDAO
from app.dao.address_dao import AddressDAO
from app.models import Property, Addresses
from app.utils.response import DAOResponse
from app.schema import PropertyResponse, PropertyBase, PropertyCreateSchema, Address, AddressBase

class PropertyDAO(BaseDAO[Property]):
    def __init__(self, model: Type[Property]):
        super().__init__(model)
        self.address_dao = AddressDAO(Addresses)

    @override
    async def create(self, db_session: AsyncSession, obj_in: Union[PropertyCreateSchema | Dict]) -> DAOResponse:

        try:
            # extract base information
            property_info = self.extract_model_data(obj_in, PropertyBase)

            # create new user
            new_property: Property = await super().create(db_session=db_session, obj_in=property_info)
            property_id = new_property.property_id

            # add additional info if exists
            address_schema = Address if 'address' in obj_in and obj_in['address'] and 'address_id' in obj_in['address'] else AddressBase
            details_methods = {
                'address': (partial(self.address_dao.add_entity_address, entity_model=self.model.__name__), address_schema)
            } 
            await self.process_entity_details(db_session, property_id, obj_in, details_methods)

            print(PropertyResponse.from_orm_model(new_property))
            return DAOResponse[PropertyResponse](success=True, data=PropertyResponse.from_orm_model(new_property))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"Fatal {str(e)}")
        
    @override
    async def get_all(self, db_session: AsyncSession) -> DAOResponse[List[PropertyResponse]]:
        result = await super().get_all(db_session=db_session)
        
        # check if no result
        if not result:
            return DAOResponse(success=True, data=[])

        return DAOResponse[List[PropertyResponse]](success=True, data=[PropertyResponse.from_orm_model(r) for r in result])
    