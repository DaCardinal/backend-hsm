from uuid import UUID
from pydantic import BaseModel, ConfigDict, constr
from typing import List, Optional, Annotated

from app.schema.media import Media, MediaBase
from app.schema.mixins.media_mixin import MediaInfoMixin


class EntityAmenitiesBase(BaseModel):
    """
    Base model for entity amenities.

    Attributes:
        amenity_id (UUID): The unique identifier for the amenity.
        property_unit_assoc_id (UUID): The unique identifier for the associated property unit.
        apply_to_units (bool): Indicates whether the amenity applies to units.
    """

    amenity_id: UUID
    property_unit_assoc_id: UUID
    apply_to_units: bool


class EntityAmenities(EntityAmenitiesBase):
    """
    Model for representing entity amenities with additional details.

    Attributes:
        id (UUID): The unique identifier for the entity amenities.
    """

    id: UUID

    model_config = ConfigDict(from_attributes=True)


class EntityAmenitiesCreate(EntityAmenitiesBase):
    """
    Schema for creating entity amenities.

    Inherits from EntityAmenitiesBase.
    """

    pass


class EntityAmenitiesUpdate(EntityAmenitiesBase):
    """
    Schema for updating entity amenities.

    Inherits from EntityAmenitiesBase.
    """

    pass


class AmenitiesBase(MediaInfoMixin):
    """
    Base model for amenities.

    Attributes:
        amenity_name (str): The name of the amenity.
        amenity_short_name (str): The short name of the amenity.
        amenity_value_type (str): The value type of the amenity.
        description (Optional[str]): The description of the amenity.
        media (Optional[List[Media] | Media]): The media associated with the amenity.
    """

    amenity_name: Annotated[str, constr(max_length=255)]
    amenity_short_name: Annotated[str, constr(max_length=50)]
    amenity_value_type: Annotated[str, constr(max_length=50)]
    description: Optional[str] = None
    media: Optional[List[Media] | Media] = []

    model_config = ConfigDict(from_attributes=True)


class Amenities(AmenitiesBase):
    """
    Model for representing amenities with additional details.

    Attributes:
        amenity_id (UUID): The unique identifier for the amenity.
    """

    amenity_id: UUID

    model_config = ConfigDict(from_attributes=True)


class AmenitiesCreateSchema(BaseModel):
    """
    Schema for creating amenities.

    Attributes:
        amenity_name (str): The name of the amenity.
        amenity_short_name (str): The short name of the amenity.
        amenity_value_type (str): The value type of the amenity.
        description (Optional[str]): The description of the amenity.
        media (Optional[List[MediaBase] | MediaBase]): The media associated with the amenity.
    """

    amenity_name: Annotated[str, constr(max_length=255)]
    amenity_short_name: Annotated[str, constr(max_length=50)]
    amenity_value_type: Annotated[str, constr(max_length=50)]
    description: Optional[str] = None
    media: Optional[List[MediaBase] | MediaBase] = []

    model_config = ConfigDict(from_attributes=True)


class AmenitiesUpdateSchema(AmenitiesBase):
    """
    Schema for updating amenities.

    Inherits from AmenitiesBase.
    """

    pass
