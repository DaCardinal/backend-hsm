from pydantic import BaseModel, Field
from typing import Any, List, Optional
from enum import Enum
from uuid import UUID

from app.models import Property as PropertyModel, Addresses, Units as UnitsModel, Amenities as AmenitiesModel, UnitsAmenities as UnitsAmenitiesModel
from app.schema import AddressBase, Address, City, Region, Country, Media, MediaBase, AmenitiesBase, Amenities, UnitsAmenitiesBase, UnitsAmenities


class PropertyStatus(str, Enum):
    available = "available"
    unavailable = "unavailable"

class PropertyType(str, Enum):
    residential = 'residential'
    commercial = 'commercial'
    industrial = 'industrial'

class PropertyType(str, Enum):
    residential = 'residential'
    commercial = 'commercial'
    industrial = 'industrial'

class PropertyUnitBase(BaseModel):
    property_unit_code: str
    property_unit_floor_space: Optional[int] = None
    property_unit_amount: Optional[float] = None
    property_floor_id: Optional[int] = None
    property_unit_notes: Optional[str] = None
    has_amenities: Optional[bool] = False

    class Config:
        from_attributes = True
        use_enum_values = True

class PropertyUnit(PropertyUnitBase):
    property_unit_id: UUID = Field(...)

    class Config:
        from_attributes = True
        use_enum_values = True

class PropertyUnitResponse(PropertyUnit):

    class Config:
        from_attributes = True
        use_enum_values = True

class PropertyUnitCreateSchema(PropertyUnitBase):
    property_id: UUID = Field(...)
    media: Optional[List[MediaBase] | MediaBase] = None

    class Config:
        from_attributes = True
        use_enum_values = True

class PropertyUnitUpdateSchema(PropertyUnit):
    media: Optional[List[Media] | Media] = None

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
    media: Optional[List[MediaBase] | MediaBase] = None
    ammenities: Optional[List[AmenitiesBase] | MediaBase] = None

    class Config:
        from_attributes = True
        use_enum_values = True

class PropertyUpdateSchema(PropertyBase):
    address: Optional[Address] = None
    media: Optional[List[Media] | Media] = None
    ammenities: Optional[List[Amenities] | Amenities] = None

    class Config:
        from_attributes = True
        use_enum_values = True

class Property(PropertyBase):
    property_id: UUID = Field(...)
    address: Optional[List[Address] | Address] = None

    class Config:
        from_attributes = True
        use_enum_values = True
    
class PropertyUnitResponse(PropertyUnit):
    media: Optional[List[Media] | Media]
    ammenities: Optional[List[Amenities] | Amenities] = None

    class Config:
        from_attributes = True
        use_enum_values = True
    
    @classmethod
    def from_orm_model(cls, property_unit: UnitsModel):
        t = cls(
            property_unit_id = property_unit.property_unit_id,
            property_unit_code = property_unit.property_unit_code,
            property_unit_floor_space = property_unit.property_unit_floor_space,
            property_unit_amount = property_unit.property_unit_amount,
            property_floor_id = property_unit.property_floor_id,
            property_unit_notes = property_unit.property_unit_notes,
            has_amenities = property_unit.has_amenities,
            media = property_unit.media
        ).model_dump()
        return t
    
class PropertyResponse(Property):
    units: Optional[List[PropertyUnit] | PropertyUnit]
    media: Optional[List[Media] | Media]
    ammenities: Optional[List[Amenities] | Amenities] = None

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
    def get_unit_ammenities(cls, unit_ammenities:List[UnitsAmenitiesModel]):
        result = []
        print(unit_ammenities)

        for unit_ammenity in unit_ammenities:
            ammenity : AmenitiesModel = unit_ammenity.ammenities
            print(ammenity)

            # result.append({
            #     'amenity_id' : ammenity.amenity_id,
            #     'amenity_name' : ammenity.amenity_name,
            #     'amenity_short_name' : ammenity.amenity_short_name,
            #     'amenity_value_type' :  ammenity.amenity_value_type
            # })
            result.append(AmenitiesModel(
                amenity_id = ammenity.amenity_id,
                amenity_name = ammenity.amenity_name,
                amenity_short_name = ammenity.amenity_short_name,
                amenity_value_type =  ammenity.amenity_value_type
            ))
        return result
    
    @classmethod
    def from_orm_model(cls, property: PropertyModel):
        print(property.ammenities)
        t = cls(
            property_id = property.property_id,
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
            address=cls.get_address_base(property.addresses),
            units=property.units,
            media=property.media,
            ammenities=cls.get_unit_ammenities(property.ammenities)
        ).model_dump()
        return t
