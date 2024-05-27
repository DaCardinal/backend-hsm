from uuid import UUID
from functools import partial
from pydantic import ValidationError
from sqlalchemy.orm import selectinload
from typing_extensions import override
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List, Type, Union

from app.dao.base_dao import BaseDAO
from app.dao.media_dao import MediaDAO
from app.utils.response import DAOResponse
from app.dao.address_dao import AddressDAO
from app.dao.ammenities_dao import AmenitiesDAO
from app.dao.property_unit_assoc_dao import PropertyUnitAssocDAO
from app.models import Property, Addresses, PropertyUnitAssoc, Media as MediaModel, Amenities as AmenitiesModel
from app.schema import PropertyResponse, PropertyBase, PropertyCreateSchema, PropertyUpdateSchema, Address, AddressBase, MediaBase, Media, Amenities, AmenitiesBase

class PropertyDAO(BaseDAO[Property]):
    def __init__(self, model: Type[Property]):
        super().__init__(model)
        self.primary_key = "property_unit_assoc_id"
        self.address_dao = AddressDAO(Addresses)
        self.property_unit_assoc_dao = PropertyUnitAssocDAO(PropertyUnitAssoc)
        self.media_dao = MediaDAO(MediaModel)
        self.ammenity_dao = AmenitiesDAO(AmenitiesModel)

    @override
    async def create(self, db_session: AsyncSession, obj_in: Union[PropertyCreateSchema | Dict]) -> DAOResponse:

        try:
            # extract base information
            property_info = self.extract_model_data(obj_in, PropertyBase)

            # create new user
            new_property: Property = await super().create(db_session=db_session, obj_in=property_info)

            # add additional info if exists
            address_schema = Address if 'address' in obj_in and obj_in['address'] and 'address_id' in obj_in['address'] else AddressBase
            ammenities_schema = Amenities if 'ammenities' in obj_in and obj_in['ammenities'] and ('amenity_id' in obj_in['ammenities'] or 'amenity_id' in obj_in['ammenities'][0]) else AmenitiesBase
            media_schema = Media if 'media' in obj_in and obj_in['media'] and ('media_id' in obj_in['media'] or 'media_id' in obj_in['media'][0]) else MediaBase
            
            # Create a link for PropertyUnitAssoc
            # property_unit_assoc_obj : PropertyUnitAssoc = await self.property_unit_assoc_dao.create(db_session = db_session, obj_in = {
            #     "property_unit_assoc_id": new_property.property_unit_assoc_id,
            #     "property_unit_type": self.model.__name__
            # })

            details_methods : dict = {
                'media': (partial(self.media_dao.add_entity_media, entity_model=self.model.__name__, entity_assoc_id=new_property.property_unit_assoc_id), media_schema),
                'ammenities': (partial(self.ammenity_dao.add_entity_ammenity, entity_model=self.model.__name__, entity_assoc_id=new_property.property_unit_assoc_id), ammenities_schema),
                'address': (partial(self.address_dao.add_entity_address, entity_model=self.model.__name__), address_schema)
            }
            if set(details_methods.keys()).issubset(set(obj_in.keys())):
                await self.process_entity_details(db_session, new_property.property_unit_assoc_id, obj_in, details_methods)
            
            new_load_addr: Property = await self.query(
                db_session=db_session,
                filters={f"{self.primary_key}":new_property.property_unit_assoc_id},
                single=True,
                options=[selectinload(Property.addresses)]
            )
            
            # commit object to db session
            await self.commit_and_refresh(db_session, new_load_addr)

            # TODO: Create a link for PropertyUnitAssoc
            return DAOResponse[PropertyResponse](success=True, data=PropertyResponse.from_orm_model(new_property))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"Fatal {str(e)}")
        
    @override
    async def update(self, db_session: AsyncSession, db_obj: Property, obj_in: PropertyUpdateSchema) -> DAOResponse[PropertyResponse]:
        try:
            # get the entity dump info
            entity_data = obj_in.model_dump()
            property_data = self.extract_model_data(obj_in.model_dump(exclude=['address', 'media', 'ammenities']), PropertyBase)

            # update property info
            existing_property : Property = await super().update(db_session=db_session, db_obj=db_obj, obj_in=PropertyBase(**property_data))
            
            # add additional info if exists
            address_schema = Address if 'address' in entity_data and entity_data['address'] and 'address_id' in entity_data['address'] else AddressBase
            media_schema = Media if 'media' in entity_data and entity_data['media'] and ('media_id' in entity_data['media'] or 'media_id' in entity_data['media'][0]) else MediaBase
            ammenities_schema = Amenities if 'ammenities' in entity_data and entity_data['ammenities'] and ('amenity_id' in entity_data['ammenities'] or 'amenity_id' in entity_data['ammenities'][0]) else AmenitiesBase

            # get the property association key
            property_unit_assoc_obj : PropertyUnitAssoc = await self.property_unit_assoc_dao.query(db_session=db_session,
                filters={f"property_unit_assoc_id":existing_property.property_unit_assoc_id},
                single=True)
            
            details_methods = {
                'media': (partial(self.media_dao.add_entity_media, entity_model=self.model.__name__, entity_assoc_id=property_unit_assoc_obj.property_unit_assoc_id), media_schema),
                'ammenities': (partial(self.ammenity_dao.add_entity_ammenity, entity_model=self.model.__name__, entity_assoc_id=property_unit_assoc_obj.property_unit_assoc_id), ammenities_schema),
                'address': (partial(self.address_dao.add_entity_address, entity_model=self.model.__name__), address_schema)
            }
            if set(details_methods.keys()).issubset(set(entity_data.keys())):
                await self.process_entity_details(db_session, existing_property.property_unit_assoc_id, entity_data, details_methods)
            
            # commit object to db session
            await self.commit_and_refresh(db_session, existing_property)
            return DAOResponse[PropertyResponse](success=True, data=PropertyResponse.from_orm_model(existing_property))
        
        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[PropertyResponse](success=False, error=f"Fatal Update {str(e)}")
    
    @override
    async def get_all(self, db_session: AsyncSession) -> DAOResponse[List[PropertyResponse]]:
        result = await super().get_all(db_session=db_session)
        
        # check if no result
        if not result:
            return DAOResponse(success=True, data=[])

        return DAOResponse[List[PropertyResponse]](success=True, data=[PropertyResponse.from_orm_model(r) for r in result])
    
    @override
    async def get(self, db_session: AsyncSession, id: Union[UUID | Any | int]) -> DAOResponse[PropertyResponse]:

        result : Property = await super().get(db_session=db_session, id=id)

        # check if no result
        if not result:
            return DAOResponse(success=True, data={})

        return DAOResponse[PropertyResponse](success=True, data=PropertyResponse.from_orm_model(result))