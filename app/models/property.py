import enum
import uuid
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Numeric, Column, ForeignKey, Boolean, Enum, Integer, String, Text, UUID,  select

from app.models.model_base import BaseModel as Base
from app.utils.lifespan import get_db as async_session
from app.models import Media, EntityMedia

# class PropertyStatus(enum.Enum):
    # lease = 'lease'
    # sold = 'sold'
    # bought = 'bought'
    # rent = 'rent'

class PropertyStatus(enum.Enum):
    available = "available"
    unavailable = "unavailable"

class PropertyType(enum.Enum):
    residential = 'residential'
    commercial = 'commercial'
    industrial = 'industrial'

class Property(Base):
    __tablename__ = 'property'
    property_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    name = Column(String(255))
    address_id = Column(UUID(as_uuid=True), ForeignKey('addresses.address_id'), nullable=True)
    # property_type = Column(UUID(as_uuid=True), ForeignKey('property_type.property_type_id'))
    property_type = Column(Enum(PropertyType))
    amount = Column(Numeric(10, 2))
    security_deposit = Column(Numeric(10, 2))
    commission = Column(Numeric(10, 2))
    floor_space = Column(Numeric(8, 2))
    num_units = Column(Integer)
    num_bathrooms = Column(Integer)
    num_garages = Column(Integer)
    has_balconies = Column(Boolean, default=False)
    has_parking_space = Column(Boolean, default=False)
    pets_allowed = Column(Boolean, default=False)
    description = Column(Text)
    property_status = Column(Enum(PropertyStatus))

    addresses = relationship(
        'Addresses',
        secondary='entity_address',
        primaryjoin="and_(Property.property_id==EntityAddress.entity_id, EntityAddress.entity_type=='Property')",
        secondaryjoin="EntityAddress.address_id==Addresses.address_id",
        overlaps="address,entity_addresses,users,properties",
        back_populates="properties",
        lazy="selectin"
    )
    units = relationship("Units",
                         secondary="property_unit_assoc",
                         primaryjoin="and_(PropertyUnitAssoc.property_id==Property.property_id)",
                         back_populates="properties", lazy="selectin")

    media = relationship("Media",
                         secondary="entity_media",
                         primaryjoin="and_(EntityMedia.entity_id==Property.property_id, EntityMedia.entity_type=='Property')",
                         overlaps="entity_media,media",
                         lazy="selectin")
    
    ammenities = relationship("UnitsAmenities",
                         secondary="property_unit_assoc",
                         primaryjoin="and_(PropertyUnitAssoc.property_id==Property.property_id, PropertyUnitAssoc.property_unit_id==Property.property_id)",
                         secondaryjoin="and_(PropertyUnitAssoc.property_unit_assoc_id==UnitsAmenities.property_unit_assoc_id)",
                         overlaps="entity_media,media,ammenities,properties,units",
                         lazy="selectin")

    async def get_media(self):        
        db_session : AsyncSession = async_session()

        async with db_session as session:
            async with session.begin():

                result = await session.execute(
                    select(Media).options(selectinload(Media.entity_media))
                    .join(EntityMedia, EntityMedia.media_id == Media.media_id)
                    .filter(EntityMedia.entity_id == self.property_id, EntityMedia.entity_type == 'Property')
                )
                property_media = result.scalars().all()
                return property_media