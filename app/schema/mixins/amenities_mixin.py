from typing import List

# schemas
from app.schema.amenity import Amenities

# models
from app.models.entity_amenities import EntityAmenities as EntityAmenitiesModel


class AmenitiesInfoMixin:
    @classmethod
    def get_amenities(
        cls, entity_amenities: List[EntityAmenitiesModel]
    ) -> List[Amenities]:
        """
        Get amenities information.

        Args:
            entity_amenities (List[EntityAmenitiesModel]): List of entity amenities models.

        Returns:
            List[Amenities]: List of amenities.
        """
        result = []

        for entity_amenity in entity_amenities:
            amenities_info: List[Amenities] | Amenities = entity_amenity.amenity

            if not isinstance(amenities_info, list):
                amenities_info = [amenities_info]

            for amenity in amenities_info:
                result.append(
                    Amenities(
                        amenity_id=amenity.amenity_id,
                        amenity_name=amenity.amenity_name,
                        amenity_short_name=amenity.amenity_short_name,
                        amenity_value_type=amenity.amenity_value_type,
                        description=amenity.description,
                        media=entity_amenity.media,
                    )
                )

        return result
