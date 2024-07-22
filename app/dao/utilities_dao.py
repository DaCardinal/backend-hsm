from uuid import UUID
from typing import List, Optional, Union
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

# utils
from app.utils.response import DAOResponse

# daos
from app.dao.base_dao import BaseDAO
from app.dao.media_dao import MediaDAO
from app.dao.payment_type_dao import PaymentTypeDAO
from app.dao.entity_media_dao import EntityMediaDAO
from app.dao.entity_billable_dao import EntityBillableDAO

# models
from app.models.payment_type import PaymentTypes
from app.models.entity_billable import EntityBillable
from app.models.utility import Utilities as UtilitiesModel

# schemas
from app.schema.billable import (
    UtilitiesBase,
    Utilities,
    EntityBillableCreate,
    EntityBillable as EntityBillableSchema,
)


class UtilitiesDAO(BaseDAO[UtilitiesModel]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.primary_key = "utility_id"

        self.model = UtilitiesModel
        self.media_dao = MediaDAO()
        self.entity_media_dao = EntityMediaDAO()
        self.payment_type_dao = PaymentTypeDAO()
        self.enity_billable_dao = EntityBillableDAO()

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    async def link_entity_to_utility(
        self,
        db_session: AsyncSession,
        entity_id: UUID,
        utility_id: UUID,
        utility_value: str,
        payment_type: str,
        entity_model=None,
    ):
        # check if payment type exists
        existing_payment_type: PaymentTypes = await self.payment_type_dao.query(
            db_session=db_session,
            filters={"payment_type_name": payment_type},
            single=True,
        )

        if not existing_payment_type:
            return DAOResponse(
                success=False, error="Payment type does not exist", data={}
            )

        entity_object = {
            "entity_assoc_id": entity_id,
            "payment_type_id": existing_payment_type.payment_type_id,
            "entity_type": entity_model if entity_model else self.model.__name__,
            "billable_assoc_id": utility_id,
            "billable_type": "Utilities",
            "billable_amount": str(utility_value),
        }

        # check if entity utility linkage exists
        entity_item: EntityBillable = await self.enity_billable_dao.query(
            db_session=db_session,
            filters={
                "entity_assoc_id": entity_id,
                "entity_type": entity_model if entity_model else self.model.__name__,
                "billable_assoc_id": utility_id,
                "billable_type": "Utilities",
            },
            single=True,
        )

        result = []

        # create entity utility linkage if it doesn't exist
        if entity_item is None:
            result = await self.enity_billable_dao.create(
                db_session=db_session, obj_in=entity_object
            )
        else:
            entity_object["billable_assoc_id"] = entity_item.billable_assoc_id
            result = await self.enity_billable_dao.update(
                db_session=db_session,
                db_obj=entity_item,
                obj_in=EntityBillableSchema(**entity_object),
            )

        return result

    async def add_entity_utility(
        self,
        db_session: AsyncSession,
        entity_id: str,
        utilities_info: Union[EntityBillableCreate | List[EntityBillableCreate]],
        entity_model=None,
        entity_assoc_id=None,
    ) -> Optional[Utilities | UtilitiesBase | List[Utilities] | List[UtilitiesBase]]:
        try:
            results = []
            entity_assoc_id = entity_assoc_id if entity_assoc_id else entity_id
            entity_model_name = entity_model if entity_model else self.model.__name__

            if not isinstance(utilities_info, list):
                utilities_info = [utilities_info]

            for utilities_item in utilities_info:
                utilities_item: EntityBillableCreate = utilities_item

                # check if the utility exists
                existing_utilities_item: Utilities = await self.query(
                    db_session=db_session,
                    filters={f"{self.primary_key}": utilities_item.billable_id},
                    single=True,
                )

                if not existing_utilities_item:
                    return DAOResponse(
                        success=False, error="Utility does not exist", data={}
                    )

                # Link entity utility id
                gen_utility_id = existing_utilities_item.utility_id
                entity_utility: EntityBillable = await self.link_entity_to_utility(
                    db_session=db_session,
                    entity_id=entity_assoc_id,
                    utility_id=gen_utility_id,
                    entity_model=entity_model_name,
                    utility_value=utilities_item.billable_amount,
                    payment_type=utilities_item.payment_type,
                )

                results.append(entity_utility)
            return results
        except NoResultFound:
            print("ERRROR:NoResultFound")
            pass
