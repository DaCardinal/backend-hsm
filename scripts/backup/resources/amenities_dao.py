from uuid import UUID
from functools import partial
from typing import List, Optional, Union
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

# daos
from app.dao.resources.base_dao import BaseDAO
from app.dao.resources.media_dao import MediaDAO
from app.dao.entities.entity_media_dao import EntityMediaDAO
from app.dao.entities.entity_amenities_dao import EntityAmenitiesDAO

# schemas
from app.schema.media import MediaCreateSchema
from app.schema.amenity import AmenitiesBase, Amenities, AmenitiesUpdateSchema

# models
from app.models.ammenity import Amenities as AmenitiesModel
from app.models.entity_amenities import EntityAmenities as EntityAmenities


# TODO
# - Add media to an amenity standalone
class AmenitiesDAO(BaseDAO[Amenities]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.primary_key = "amenity_id"
        self.model = AmenitiesModel

        self.media_dao = MediaDAO()
        self.entity_media_dao = EntityMediaDAO()
        self.entity_amenities_dao = EntityAmenitiesDAO()

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    async def link_entity_to_ammenity(
        self,
        db_session: AsyncSession,
        property_unit_assoc_id: UUID,
        ammenity_id: UUID,
        entity_model=None,
    ):
        entity_amenity_object = {
            "entity_assoc_id": property_unit_assoc_id,
            "entity_type": entity_model if entity_model else self.model.__name__,
            "amenity_id": ammenity_id,
        }

        # check if entity amenity linkage exists
        result = await self.entity_amenities_dao.query(
            db_session=db_session, filters={**entity_amenity_object}, single=True
        )

        # create entity amenity linkage if it doesn't exist
        if result is None:
            result = await self.entity_amenities_dao.create(
                db_session=db_session, obj_in=entity_amenity_object
            )

        return result

    async def add_entity_ammenity(
        self,
        db_session: AsyncSession,
        entity_id: str,
        amenities_info: Union[
            Amenities | AmenitiesBase | List[Amenities] | List[AmenitiesBase]
        ],
        entity_model=None,
        entity_assoc_id=None,
    ) -> Optional[Amenities | AmenitiesBase | List[Amenities] | List[AmenitiesBase]]:
        try:
            results = []
            entity_model_name = entity_model if entity_model else self.model.__name__
            entity_assoc_id = entity_assoc_id if entity_assoc_id else entity_id

            if not isinstance(amenities_info, list):
                amenities_info = [amenities_info]

            for amenities_item in amenities_info:
                amenities_item: Amenities = amenities_item

                # Check if the entity already exists
                existing_amenities_item = await self.query(
                    db_session=db_session,
                    filters={**amenities_item.model_dump(exclude=["media"])},
                    single=True,
                )

                if existing_amenities_item:
                    obj_data = self.extract_model_data(
                        amenities_item.model_dump(exclude=["media"]), Amenities
                    )
                    obj_data["amenity_id"] = existing_amenities_item.amenity_id
                    gen_amenity_id = existing_amenities_item.amenity_id

                    # create amenitites models
                    crud_media_item: AmenitiesModel = await self.update(
                        db_session=db_session,
                        db_obj=existing_amenities_item,
                        obj_in=AmenitiesUpdateSchema(**obj_data),
                    )
                else:
                    # Creating an ammenity
                    crud_media_item: Amenities = await self.create(
                        db_session=db_session,
                        obj_in=amenities_item.model_dump(exclude=["media"]),
                    )
                    gen_amenity_id = crud_media_item.amenity_id

                # Link entity amenity id
                entity_amenity: EntityAmenities = await self.link_entity_to_ammenity(
                    db_session=db_session,
                    property_unit_assoc_id=entity_assoc_id,
                    ammenity_id=gen_amenity_id,
                    entity_model=entity_model_name,
                )

                # Link entity media id
                details_methods: dict = {
                    "media": (
                        partial(
                            self.media_dao.add_entity_media,
                            entity_model="EntityAmenities",
                            entity_assoc_id=entity_amenity.entity_amenities_id,
                        ),
                        MediaCreateSchema,
                    )
                }
                await self.process_entity_details(
                    db_session,
                    entity_amenity.entity_amenities_id,
                    amenities_item.model_dump(),
                    details_methods,
                )

                results.append(crud_media_item)
            return results
        except NoResultFound:
            # TODO: Remove this
            print("ERRROR:NoResultFound")
            pass
