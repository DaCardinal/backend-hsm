from sqlalchemy import Numeric, create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base
import enum

class PropertyStatus(enum.Enum):
    lease = 'lease'
    sold = 'sold'
    bought = 'bought'
    rent = 'rent'

class PropertyType(enum.Enum):
    lease = 'lease'
    sold = 'sold'
    bought = 'bought'
    rent = 'rent'
    
class Property(Base):
    __tablename__ = 'property'
    property_id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(255))
    city_id = Column(UUID(as_uuid=True), ForeignKey('city.city_id'))
    property_type_id = Column(UUID(as_uuid=True), ForeignKey('property_type.property_type_id'))
    amount = Column(Numeric(10, 2))
    security_deposit = Column(Numeric(10, 2))
    commission = Column(Numeric(10, 2))
    floor_space = Column(Numeric(8, 2))
    num_balconies = Column(Integer)
    num_unit_rooms = Column(Integer)
    num_bathrooms = Column(Integer)
    num_garages = Column(Integer)
    num_parking_space = Column(Integer)
    pets_allowed = Column(Boolean, default=False)
    description = Column(Text)
    property_status = Column(Enum(PropertyStatus))
