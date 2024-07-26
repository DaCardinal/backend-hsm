from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Union

# schemas
from app.schema.enums import ContractStatus
from app.schema.mixins.user_mixins import UserBaseMixin, UserBase
from app.schema.mixins.billable_mixin import UtilitiesMixin
from app.schema.mixins.property_mixin import (
    PropertyDetailsMixin,
    Property,
    PropertyUnit,
)


# models
from app.models.contract import Contract as ContractModel
from app.models.under_contract import UnderContract as UnderContractModel


class UserContract(BaseModel):
    """
    Base schema for representing contract information.

    Attributes:
        contract_id (UUID): The unique identifier for the contract.
        contract_type (str): The type of the contract.
        payment_type (str): The type of payment for the contract.
        contract_status (ContractStatus): The status of the contract.
        contract_details (str): The details of the contract.
        num_invoices (int): The number of invoices for the contract.
        payment_amount (int): The payment amount for the contract.
        fee_percentage (int): The fee percentage for the contract.
        fee_amount (int): The fee amount for the contract.
        date_signed (datetime): The date the contract was signed.
        start_date (Optional[datetime]): The start date of the contract.
        end_date (Optional[datetime]): The end date of the contract.
    """

    contract_id: UUID
    contract_type: str
    payment_type: str
    contract_status: ContractStatus
    contract_details: str
    num_invoices: int
    payment_amount: int
    fee_percentage: int
    fee_amount: int
    date_signed: datetime = datetime.now()
    start_date: Optional[datetime] = datetime.now()
    end_date: Optional[datetime] = datetime.now()
    properties: Optional[List[Union[Property, PropertyUnit]]] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UnderContractSchema(BaseModel):
    """
    Schema for representing an under-contract relationship.

    Attributes:
        under_contract_id (Optional[UUID]): The unique identifier for the under-contract relationship.
        property_unit_assoc (Optional[UUID | Property | PropertyUnit]): The associated property or property unit.
        contract_id (Optional[UUID]): The unique identifier for the contract.
        contract_status (Optional[ContractStatus]): The status of the contract.
        client_id (Optional[UUID | UserBase]): The unique identifier for the client.
        employee_id (Optional[UUID | UserBase]): The unique identifier for the employee.
    """

    under_contract_id: Optional[UUID] = None
    property_unit_assoc: Optional[UUID | Property | PropertyUnit] = None
    contract_id: Optional[UUID | str] = None
    contract_status: Optional[ContractStatus] = None
    client_id: Optional[UUID | UserBase] = None
    employee_id: Optional[UUID | UserBase] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    next_payment_due: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class ContractInfoMixin(PropertyDetailsMixin, UserBaseMixin, UtilitiesMixin):
    @classmethod
    def get_contract_details(cls, contract_details: List[UnderContractModel]):
        """
        Get contract details.

        Args:
            contract_details (List[UnderContract]): List of contract details.

        Returns:
            List[UnderContractSchema]: List of under-contract schema objects.
        """
        result = []

        for contract_detail in contract_details:
            property_unit_assoc_query = cls.get_property_details(
                [contract_detail.properties]
            )

            result.append(
                UnderContractSchema(
                    under_contract_id=contract_detail.under_contract_id,
                    property_unit_assoc=property_unit_assoc_query[0]
                    if len(property_unit_assoc_query) != 0
                    else None,
                    contract_id=contract_detail.contract_id,
                    contract_status=contract_detail.contract_status,
                    client_id=cls.get_user_info(contract_detail.client_representative),
                    employee_id=cls.get_user_info(
                        contract_detail.employee_representative
                    ),
                    start_date=contract_detail.start_date,
                    end_date=contract_detail.end_date,
                    next_payment_due=contract_detail.next_payment_due,
                )
            )

        return result

    @classmethod
    def get_contract_info(
        cls, contract_info: List[UnderContractModel]
    ) -> List[UserContract]:
        """
        Get contract information.

        Args:
            contract_info (List[UnderContract]): List of contract information.

        Returns:
            List[ContractBase]: List of contract base objects.
        """
        result = []

        for under_contract in contract_info:
            contract: ContractModel = under_contract.contract

            if contract:
                result.append(
                    UserContract(
                        contract_id=contract.contract_id,
                        num_invoices=contract.num_invoices,
                        contract_type=contract.contract_type_value,
                        payment_type=contract.payment_type_value,
                        contract_status=contract.contract_status,
                        contract_details=contract.contract_details,
                        payment_amount=contract.payment_amount,
                        fee_percentage=contract.fee_percentage,
                        fee_amount=contract.fee_amount,
                        date_signed=contract.date_signed,
                        start_date=contract.start_date,
                        end_date=contract.end_date,
                        properties=contract.properties,
                        property_unit_assoc_id=under_contract.property_unit_assoc_id,
                        next_payment_due=under_contract.next_payment_due,
                    )
                )
        return result
