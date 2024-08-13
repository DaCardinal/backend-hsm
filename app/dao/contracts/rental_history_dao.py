from typing import List, Union
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

# dao
from app.dao.resources.base_dao import BaseDAO
from app.dao.address.address_dao import AddressDAO

# models
from app.models.rental_history import PastRentalHistory as PastRentalHistoryModel

# schemas
from app.schema.mixins.user_mixins import (
    PastRentalHistoryBase,
    PastRentalHistory,
    PastRentalHistoryCreateSchema,
    PastRentalHistoryResponse,
)

# utils
from app.utils.response import DAOResponse


class PastRentalHistoryDAO(BaseDAO[PastRentalHistoryModel]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = PastRentalHistoryModel
        self.primary_key = "rental_history_id"
        self.address_dao = AddressDAO()

        self.detail_mappings = {
            "address": self.address_dao.add_entity_address,
        }

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    async def create_or_update_rental_history_entity(
        self,
        db_session: AsyncSession,
        entity_object: Union[PastRentalHistoryBase | PastRentalHistory],
    ) -> PastRentalHistoryModel:
        entity_item = None
        print("here")

        if "rental_history_id" in entity_object.model_dump():
            entity_item = await self.query(
                db_session=db_session,
                filters={f"{self.primary_key}": entity_object.rental_history_id},
                single=True,
            )

        if entity_item:
            print("updating")
            return await self.update(
                db_session=db_session,
                db_obj=entity_item,
                obj_in=PastRentalHistoryCreateSchema(
                    **entity_object.model_dump(exclude=["address"])
                ),
            )
        else:
            print("creating")
            return await self.create(
                db_session=db_session,
                obj_in=entity_object.model_dump(exclude=["address"]),
            )

    async def add_entity_rental_history(
        self,
        db_session: AsyncSession,
        entity_id: str,
        rental_history_info: Union[
            PastRentalHistoryBase
            | PastRentalHistory
            | List[PastRentalHistoryBase | PastRentalHistory]
        ],
    ) -> DAOResponse[List[PastRentalHistoryBase | PastRentalHistory]]:
        try:
            results = []

            rental_history_info = (
                rental_history_info
                if isinstance(rental_history_info, list)
                else [rental_history_info]
            )

            for rental_history in rental_history_info:
                crud_rental_history_item = (
                    await self.create_or_update_rental_history_entity(
                        db_session=db_session, entity_object=rental_history
                    )
                )

                # process any entity details
                await self.handle_entity_details(
                    db_session=db_session,
                    entity_data=rental_history.model_dump(),
                    detail_mappings=self.detail_mappings,
                    entity_model=PastRentalHistory.__name__,
                    entity_assoc_id=crud_rental_history_item.address_hash
                    or entity_id,  # TODO (DQ): Check this
                )

                results.append(crud_rental_history_item)

            return DAOResponse(
                success=True,
                data=[PastRentalHistoryResponse.from_orm_model(r) for r in results],
            )
        except NoResultFound as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(
                success=False, error=f"Rental History DAO Error: {str(e)}"
            )
