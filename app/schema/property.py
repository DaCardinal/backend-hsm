from pydantic import BaseModel, UUID4, constr
from typing import Optional
from enum import Enum

class PropertyStatus(str, Enum):
    lease = 'lease'
    sold = 'sold'
    bought = 'bought'
    rent = 'rent'

class PropertyType(str, Enum):
    residential = 'residential'
    commercial = 'commercial'
    industrial = 'industrial'

class Property(BaseModel):
    name: str
    property_type: PropertyType
    amount: float
    security_deposit: Optional[float] = None
    commission: Optional[float] = None
    floor_space: Optional[float] = None
    num_balconies: Optional[int] = None
    num_unit_rooms: Optional[int] = None
    num_bathrooms: Optional[int] = None
    num_garages: Optional[int] = None
    num_parking_space: Optional[int] = None
    pets_allowed: bool = False
    description: Optional[str] = None
    property_status: PropertyStatus

    class Config:
        from_attributes = True
