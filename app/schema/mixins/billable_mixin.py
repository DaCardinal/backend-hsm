from uuid import UUID
from typing import List
from pydantic import BaseModel, ConfigDict

# schemas
from app.schema.billable import Utilities, EntityBillable

# models
from app.models.payment_type import PaymentTypes as PaymentTypeModel
from app.models.entity_billable import EntityBillable as EntityBillableModel


class UtilityInfo(BaseModel):
    utility: str
    frequency: str
    billable_amount: float
    apply_to_units: bool
    entity_utilities_id: UUID

    model_config = ConfigDict(from_attributes=True)


class UtilitiesMixin:
    @classmethod
    def get_utilities_info(cls, utilities: List[EntityBillable]):
        """
        Get utilities information.

        Args:
            utilities (List[EntityBillable]): List of entity billable objects.

        Returns:
            List[Dict[str, Any]]: List of utility information.
        """
        result = []

        for entity_utility in utilities:
            entity_utility: EntityBillableModel = entity_utility
            payment_type: PaymentTypeModel = entity_utility.payment_type
            utility: Utilities = entity_utility.utility

            result.append(
                UtilityInfo(
                    utility=utility.name,
                    frequency=payment_type.payment_type_name,
                    billable_amount=entity_utility.billable_amount,
                    apply_to_units=entity_utility.apply_to_units,
                    entity_utilities_id=entity_utility.billable_assoc_id,
                )
            )

        return result
