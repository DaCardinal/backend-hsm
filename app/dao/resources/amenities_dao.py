from uuid import UUID
from typing import List, Optional, Union
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

# daos
from app.dao.resources.base_dao import BaseDAO
from app.dao.resources.media_dao import MediaDAO
from app.dao.entities.entity_media_dao import EntityMediaDAO
from app.dao.entities.entity_amenities_dao import EntityAmenitiesDAO

# schemas
from app.schema.amenity import AmenitiesBase, Amenities, AmenitiesUpdateSchema

# models
from app.models.ammenity import Amenities as AmenitiesModel
from app.models.entity_amenities import EntityAmenities as EntityAmenities

# utils
from app.utils.response import DAOResponse


# TODO
# - Add media to an amenity standalone
class AmenitiesDAO(BaseDAO[Amenities]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.primary_key = "amenity_id"
        self.model = AmenitiesModel

        self.media_dao = MediaDAO()
        self.entity_media_dao = EntityMediaDAO()
        self.entity_amenities_dao = EntityAmenitiesDAO()
        self.detail_mappings = {"media": self.media_dao.add_entity_media}

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    async def associate_entity_to_ammenity(
        self,
        db_session: AsyncSession,
        entity_id: UUID,
        ammenity_id: UUID,
        entity_model=None,
    ):
        entity_model_name = entity_model or self.model.__name__

        entity_amenity_object = {
            "entity_assoc_id": entity_id,
            "entity_type": entity_model_name,
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

    async def create_or_update_amenity(
        self, db_session: AsyncSession, amenities_item: Union[Amenities | AmenitiesBase]
    ) -> Union[Amenities | AmenitiesBase]:
        # check if the amenity already exists
        existing_amenities_item: Union[Amenities | None] = await self.query(
            db_session=db_session,
            filters={**amenities_item.model_dump(exclude=["media"])},
            single=True,
        )

        if existing_amenities_item:
            obj_data = self.extract_model_data(
                amenities_item.model_dump(exclude=["media"]), Amenities
            )
            obj_data["amenity_id"] = existing_amenities_item.amenity_id

            # update existing entity linkage
            return await self.update(
                db_session=db_session,
                db_obj=existing_amenities_item,
                obj_in=AmenitiesUpdateSchema(**obj_data),
            )
        else:
            # create new entity linkage
            return await self.create(
                db_session=db_session,
                obj_in=amenities_item.model_dump(exclude=["media"]),
            )

    async def add_entity_ammenity(
        self,
        db_session: AsyncSession,
        entity_id: str,
        amenities_info: Union[
            Amenities | AmenitiesBase | List[Amenities] | List[AmenitiesBase]
        ],
        entity_model: Union[str | None] = None,
        entity_assoc_id: Union[UUID | None] = None,
    ) -> Optional[Amenities | AmenitiesBase | List[Amenities] | List[AmenitiesBase]]:
        try:
            results = []
            entity_model_name = entity_model if entity_model else self.model.__name__
            entity_assoc_id = entity_assoc_id if entity_assoc_id else entity_id
            amenities_info = (
                amenities_info if isinstance(amenities_info, list) else [amenities_info]
            )

            for amenities_item in amenities_info:
                crud_amenities_item = await self.create_or_update_amenity(
                    db_session=db_session, amenities_item=amenities_item
                )

                # Link entity amenity id
                entity_amenity: EntityAmenities = (
                    await self.associate_entity_to_ammenity(
                        db_session=db_session,
                        entity_id=entity_assoc_id,
                        ammenity_id=crud_amenities_item.amenity_id,
                        entity_model=entity_model_name,
                    )
                )

                # process any entity details and link entity media id
                await self.handle_entity_details(
                    db_session=db_session,
                    entity_data=amenities_item.model_dump(),
                    detail_mappings=self.detail_mappings,
                    entity_model="EntityAmenities",
                    entity_assoc_id=entity_amenity.entity_amenities_id,
                )

                results.append(crud_amenities_item)

            return results
        except NoResultFound as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"Amenity DAO Error: {str(e)}")
