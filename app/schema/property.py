from pydantic import BaseModel, Field
from typing import Any, List, Optional
from enum import Enum
from uuid import UUID

from app.models import Property as PropertyModel, Addresses, Units as UnitsModel, Utilities as UtilityModel, EntityAmenities as EntityAmenitiesModel, EntityBillable as EntityBillableModel, PaymentTypes
from app.schema import AddressBase, Address, City, Region, Country, Media, MediaBase, AmenitiesBase, Amenities, Utilities, AmenitiesCreateSchema, EntityBillableCreate, EntityBillable

class PropertyStatus(str, Enum):
    available = "available"
    unavailable = "unavailable"

class PropertyType(str, Enum):
    residential = 'residential'
    commercial = 'commercial'
    industrial = 'industrial'

class PropertyUnitBase(BaseModel):
    property_unit_code: Optional[str] = None
    property_unit_floor_space: Optional[int] = None
    property_unit_amount: Optional[float] = None
    property_floor_id: Optional[int] = None
    property_unit_notes: Optional[str] = None
    property_unit_security_deposit: Optional[float] = None
    property_unit_commission: Optional[float] = None
    has_amenities: Optional[bool] = False
    property_id: UUID = Field(...)

    class Config:
        from_attributes = True
        use_enum_values = True

class PropertyUnit(PropertyUnitBase):
    property_unit_assoc_id: Optional[UUID]
    # property_unit_id: UUID = Field(...)

    class Config:
        from_attributes = True
        use_enum_values = True

class PropertyUnitCreateSchema(PropertyUnitBase):
    # property_id: UUID = Field(...)
    media: Optional[List[Media] | List[MediaBase] | Media | MediaBase] = None
    amenities: Optional[List[AmenitiesCreateSchema] | AmenitiesCreateSchema] = None
    utilities: Optional[List[EntityBillableCreate] | EntityBillableCreate] = None

    class Config:
        from_attributes = True
        use_enum_values = True

class PropertyUnitUpdateSchema(PropertyUnit):
    media: Optional[List[Media] | Media] = None
    amenities: Optional[List[Amenities] | Amenities] = None
    utilities: Optional[List[EntityBillableCreate] | EntityBillableCreate] = None

    class Config:
        from_attributes = True
        use_enum_values = True

class PropertyBase(BaseModel):
    name: str
    property_type: PropertyType = Field(...)
    amount: float
    security_deposit: Optional[float] = None
    commission: Optional[float] = None
    floor_space: Optional[float] = None
    num_units: Optional[int] = None
    num_bathrooms: Optional[int] = None
    num_garages: Optional[int] = None
    has_balconies: Optional[bool] = False
    has_parking_space: Optional[bool] = False
    pets_allowed: bool = False
    description: Optional[str] = None
    property_status: PropertyStatus = Field(...)

    class Config:
        from_attributes = True
        use_enum_values = True

class PropertyCreateSchema(PropertyBase):
    address: Optional[AddressBase] = None
    media: Optional[List[Media] | List[MediaBase] | Media | MediaBase] = None
    # amenities: Optional[List[Amenities] | List[AmenitiesBase] | Amenities | AmenitiesBase] = None
    amenities: Optional[List[AmenitiesCreateSchema] | AmenitiesCreateSchema] = None
    utilities: Optional[List[EntityBillableCreate] | EntityBillableCreate] = None

    class Config:
        from_attributes = True
        use_enum_values = True

class PropertyUpdateSchema(PropertyBase):
    address: Optional[Address] = None
    media: Optional[List[Media] | Media] = None
    amenities: Optional[List[Amenities] | Amenities] = None
    utilities: Optional[List[EntityBillableCreate] | EntityBillableCreate] = None

    class Config:
        from_attributes = True
        use_enum_values = True

class PropertyUnitAssoc(BaseModel):
    property_unit_assoc_id: Optional[UUID]
    property_unit_type: Optional[str]
    # property_id: Optional[UUID]
    # property_unitid: Optional[UUID]
    # property: Optional[PropertyBase]

    class Config:
        from_attributes = True
        use_enum_values = True

class Property(PropertyBase):
    property_unit_assoc_id: Optional[UUID]
    # property_id: UUID = Field(...)
    address: Optional[List[Address] | Address] = None

    class Config:
        from_attributes = True
        use_enum_values = True
    
class PropertyUnitResponse(PropertyUnit):
    media: Optional[List[Media] | Media]
    property: Optional[PropertyBase]
    amenities: Optional[List[Amenities] | Amenities] = None
    utilities: Optional[List[Any]] = None

    class Config:
        from_attributes = True
        use_enum_values = True
    
    @classmethod
    def get_amenitites(cls, entity_amenitites:List[EntityAmenitiesModel]):
        result = []

        for entity_amenitity in entity_amenitites:
            amenities_info = entity_amenitity.amenity

            if not isinstance(amenities_info, list):
                amenities_info = [amenities_info]
            
            for amenity in amenities_info:
                amenity : Amenities = amenity

                result.append(Amenities(
                    amenity_id=amenity.amenity_id,
                    amenity_name = amenity.amenity_name,
                    amenity_short_name = amenity.amenity_short_name,
                    amenity_value_type = amenity.amenity_value_type,
                    description = amenity.description, 
                    media = entity_amenitity.media
                ))
            
        return result
    
    @classmethod
    def get_utilities_info(cls, utilities: List[EntityBillable]):
        result = []

        for entity_utility in utilities:
            entity_utility : EntityBillableModel = entity_utility
            payment_type: PaymentTypes = entity_utility.payment_type
            utility : Utilities = entity_utility.utility

            result.append({
                "utility": utility.name,
                "payment_type": payment_type.payment_type_name,
                "utility_value": entity_utility.billable_amount,
                "apply_to_units": False,
                "entity_utilities_id": entity_utility.billable_assoc_id
            })
        return result
    
    @classmethod
    def from_orm_model(cls, property_unit: UnitsModel):

        return cls(
            property_unit_assoc_id = property_unit.property_unit_assoc_id,
            property_unit_code = property_unit.property_unit_code,
            property_unit_floor_space = property_unit.property_unit_floor_space,
            property_unit_amount = property_unit.property_unit_amount,
            property_floor_id = property_unit.property_floor_id,
            property_unit_notes = property_unit.property_unit_notes,
            has_amenities = property_unit.has_amenities,
            property_id = property_unit.property_id,
            property_unit_security_deposit = property_unit.property_unit_security_deposit,
            property_unit_commission = property_unit.property_unit_commission,
            property = property_unit.property,
            media = property_unit.media,
            amenities=cls.get_amenitites(property_unit.entity_amenities),
            utilities=cls.get_utilities_info(property_unit.utilities)
        ).model_dump()
    
class PropertyResponse(Property):
    units: Optional[List[PropertyUnit] | PropertyUnit]
    media: Optional[List[Media] | Media]
    amenities: Optional[List[Amenities] | Amenities] = None
    utilities: Optional[List[Any]] = None

    class Config:
        from_attributes = True
        use_enum_values = True

    @classmethod
    def get_address_base(cls, address:List[Addresses]):
        result = []

        for addr in address:
            addr_city : City = addr.city
            addr_region : Region = addr.region
            addr_country : Country = addr.country

            result.append(Address(
                address_id = addr.address_id,
                address_type = addr.address_type,
                primary = addr.primary,
                address_1 = addr.address_1,
                address_2 = addr.address_2,
                address_postalcode = addr.address_postalcode,
                city = addr_city.city_name,
                region = addr_region.region_name,
                country = addr_country.country_name
            ))
        return result
    
    @classmethod
    def get_utilities_info(cls, utilities: List[EntityBillable]):
        result = []

        for entity_utility in utilities:
            entity_utility : EntityBillableModel = entity_utility
            payment_type: PaymentTypes = entity_utility.payment_type
            utility : Utilities = entity_utility.utility

            result.append({
                "utility": utility.name,
                "payment_type": payment_type.payment_type_name,
                "utility_value": entity_utility.billable_amount,
                "apply_to_units": False,
                "entity_utilities_id": entity_utility.billable_assoc_id
            })
        return result
    
    @classmethod
    def get_amenitites(cls, entity_amenitites:List[EntityAmenitiesModel]):
        result = []

        for entity_amenitity in entity_amenitites:
            amenities_info = entity_amenitity.amenity

            if not isinstance(amenities_info, list):
                amenities_info = [amenities_info]
            
            for amenity in amenities_info:
                amenity : Amenities = amenity

                result.append(Amenities(
                    amenity_id=amenity.amenity_id,
                    amenity_name = amenity.amenity_name,
                    amenity_short_name = amenity.amenity_short_name,
                    amenity_value_type = amenity.amenity_value_type,
                    description = amenity.description, 
                    media = entity_amenitity.media
                ))
            
        return result
    
    @classmethod
    def from_orm_model(cls, property: PropertyModel):

        return cls(
            name = property.name,
            property_type = property.property_type,
            amount = property.amount,
            security_deposit = property.security_deposit,
            commission = property.commission,
            floor_space = property.floor_space,
            num_units = property.num_units,
            num_bathrooms = property.num_bathrooms,
            num_garages = property.num_garages,
            has_balconies = property.has_balconies,
            has_parking_space = property.has_parking_space,
            pets_allowed = property.pets_allowed,
            description = property.description,
            property_status = property.property_status,
            property_unit_assoc_id =property.property_unit_assoc_id,
            address=cls.get_address_base(property.addresses),
            units=property.units,
            media=property.media,
            amenities=cls.get_amenitites(property.entity_amenities),
            utilities=cls.get_utilities_info(property.utilities)
        ).model_dump()
