from uuid import UUID
from typing import Any, Dict, List, Union
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

# utils
from app.utils.response import DAOResponse

# daos
from app.dao.resources.base_dao import BaseDAO
from app.dao.resources.media_dao import MediaDAO
from app.dao.billing.payment_type_dao import PaymentTypeDAO
from app.dao.entities.entity_media_dao import EntityMediaDAO
from app.dao.entities.entity_billable_dao import EntityBillableDAO

# models
from app.models.payment_type import PaymentTypes
from app.models.entity_billable import EntityBillable
from app.models.utility import Utilities as UtilitiesModel

# schemas
from app.schema.billable import (
    Billable,
    EntityBillableResponse,
    Utilities,
    EntityBillable as EntityBillableSchema,
)


class UtilitiesDAO(BaseDAO[UtilitiesModel]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.primary_key = "utility_id"

        self.model = UtilitiesModel
        self.media_dao = MediaDAO()
        self.entity_media_dao = EntityMediaDAO()
        self.payment_type_dao = PaymentTypeDAO()
        self.entity_billable_dao = EntityBillableDAO()

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    async def create_or_update_billable_entity(
        self, db_session: AsyncSession, entity_object: Dict[str, Any]
    ) -> EntityBillable:
        # check if the entity utility linkage exists
        entity_item: EntityBillable = await self.entity_billable_dao.query(
            db_session=db_session,
            filters={
                "entity_type": entity_object["entity_type"],
                "billable_type": entity_object["billable_type"],
                "entity_assoc_id": entity_object["entity_assoc_id"],
                "billable_assoc_id": entity_object["billable_assoc_id"],
            },
            single=True,
        )

        if entity_item:
            entity_object["entity_billable_id"] = entity_item.entity_billable_id
            # update existing entity linkage
            return await self.entity_billable_dao.update(
                db_session=db_session,
                db_obj=entity_item,
                obj_in=EntityBillableSchema(**entity_object),
            )
        else:
            # create new entity linkage
            return await self.entity_billable_dao.create(
                db_session=db_session, obj_in=entity_object
            )

    async def associate_billable_with_entity(
        self,
        db_session: AsyncSession,
        entity_id: UUID,
        utility_id: UUID,
        utility_value: str,
        payment_type: str,
        entity_model: str = None,
    ):
        # check if payment type exists
        existing_payment_type: PaymentTypes = (
            await self.payment_type_dao.get_existing_payment_type(
                db_session, payment_type
            )
        )

        if not existing_payment_type:
            return DAOResponse(
                success=False, error="Payment type does not exist", data={}
            )

        entity_model_name = entity_model or self.model.__name__

        entity_object = {
            "entity_assoc_id": entity_id,
            "payment_type_id": existing_payment_type.payment_type_id,
            "entity_type": entity_model_name,
            "billable_assoc_id": utility_id,
            "billable_type": "Utilities",
            "billable_amount": str(utility_value),
        }

        # link the billable entity
        return await self.create_or_update_billable_entity(db_session, entity_object)

    async def add_entity_utility(
        self,
        db_session: AsyncSession,
        entity_id: str,
        utilities_info: Union[Billable | List[Billable]],
        entity_model: Union[str | None] = None,
        entity_assoc_id: Union[UUID | None] = None,
    ) -> DAOResponse[List[EntityBillable | Dict]]:
        try:
            results = []
            entity_assoc_id = entity_assoc_id or entity_id
            entity_model_name = entity_model or self.model.__name__
            utilities_info = (
                utilities_info if isinstance(utilities_info, list) else [utilities_info]
            )

            for utilities_item in utilities_info:
                # check if utility exists
                existing_utilities_item: Union[Utilities | None] = await self.query(
                    db_session=db_session,
                    filters={f"{self.primary_key}": utilities_item.billable_id},
                    single=True,
                )

                if not existing_utilities_item:
                    raise NoResultFound("Utility does not exist")

                entity_utility: EntityBillable = (
                    await self.associate_billable_with_entity(
                        db_session=db_session,
                        entity_id=entity_assoc_id,
                        utility_id=existing_utilities_item.utility_id,
                        entity_model=entity_model_name,
                        utility_value=utilities_item.billable_amount,
                        payment_type=utilities_item.payment_type,
                    )
                )
                results.append(entity_utility)

            return DAOResponse(
                success=True,
                data=[EntityBillableResponse.from_orm_model(r) for r in results],
            )
        except NoResultFound as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"Utility DAO Error: {str(e)}")
