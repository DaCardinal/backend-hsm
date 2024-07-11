from uuid import UUID
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, constr
from typing import Any, List, Optional, Annotated

# schemas
from app.schema.user import UserBase, User
from app.schema.enums import ContractStatus
from app.schema.property import Property, PropertyUnit
from app.schema.under_contract import UnderContractSchema
from app.schema.billable import Utilities, EntityBillable, EntityBillableCreate

# models
from app.models.contract import Contract as ContractModel
from app.models.payment_type import PaymentTypes as PaymentTypeModel
from app.models.under_contract import UnderContract as UnderContractModel
from app.models.entity_billable import EntityBillable as EntityBillableModel


# schema
# EntityBillableCreate, EntityBillable, Utilities

# models
# EntityBillableModel, ContractModel, UnderContractModel
# from app.models import PropertyUnitAssoc, Contract, User 
# 
#TODO: Verify works, review importance of UnderContract and UnderContractSchema


class ContractType(BaseModel):
    """
    Schema for representing a contract type.

    Attributes:
        contract_type_id (UUID): The unique identifier for the contract type.
        contract_type_name (Optional[str]): The name of the contract type (max length 128).
        fee_percentage (Optional[Decimal]): The fee percentage for the contract type.
    """
    contract_type_id: UUID
    contract_type_name: Optional[Annotated[str, constr(max_length=128)]] = None
    fee_percentage: Optional[Decimal] = None

    class Config:
        from_attributes = True


class ContractBase(BaseModel):
    """
    Base schema for representing contract information.

    Attributes:
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

    class Config:
        from_attributes = True
        use_enum_values = True


class Contract(ContractBase):
    """
    Model for representing a contract with additional details.

    Attributes:
        contract_id (UUID): The unique identifier for the contract.
    """
    contract_id: UUID

    class Config:
        from_attributes = True


class ContractCreateSchema(BaseModel):
    """
    Schema for creating a new contract.

    Attributes:
        contract_type (str): The type of the contract.
        payment_type (str): The type of payment for the contract.
        contract_status (ContractStatus): The status of the contract.
        contract_details (Optional[str]): The details of the contract.
        payment_amount (Decimal): The payment amount for the contract.
        fee_percentage (Optional[Decimal]): The fee percentage for the contract.
        fee_amount (Optional[Decimal]): The fee amount for the contract.
        date_signed (datetime): The date the contract was signed.
        start_date (Optional[datetime]): The start date of the contract.
        end_date (Optional[datetime]): The end date of the contract.
        contract_info (Optional[List[UnderContractSchema] | UnderContractSchema]): The information of the under-contract relationships.
        utilities (Optional[List[EntityBillableCreate] | EntityBillableCreate]): The utilities associated with the contract.
    """
    contract_type: str
    payment_type: str
    contract_status: ContractStatus
    contract_details: Optional[str] = None
    payment_amount: Decimal
    fee_percentage: Optional[Decimal] = None
    fee_amount: Optional[Decimal] = None
    date_signed: datetime = datetime.now()
    start_date: Optional[datetime] = datetime.now()
    end_date: Optional[datetime] = datetime.now()
    contract_info: Optional[List[UnderContractSchema] | UnderContractSchema] = None
    utilities: Optional[List[EntityBillableCreate] | EntityBillableCreate] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class ContractUpdateSchema(BaseModel):
    """
    Schema for updating an existing contract.

    Attributes:
        contract_type (Optional[str]): The type of the contract.
        payment_type (Optional[str]): The type of payment for the contract.
        contract_status (Optional[ContractStatus]): The status of the contract.
        contract_details (Optional[str]): The details of the contract.
        payment_amount (Optional[Decimal]): The payment amount for the contract.
        fee_percentage (Optional[Decimal]): The fee percentage for the contract.
        fee_amount (Optional[Decimal]): The fee amount for the contract.
        date_signed (Optional[datetime]): The date the contract was signed.
        start_date (Optional[datetime]): The start date of the contract.
        end_date (Optional[datetime]): The end date of the contract.
        contract_info (Optional[List[UnderContractSchema] | UnderContractSchema]): The information of the under-contract relationships.
        utilities (Optional[List[EntityBillableCreate] | EntityBillableCreate]): The utilities associated with the contract.
    """
    contract_type: Optional[str] = None
    payment_type: Optional[str] = None
    contract_status: Optional[ContractStatus] = None
    contract_details: Optional[str] = None
    payment_amount: Optional[Decimal] = None
    fee_percentage: Optional[Decimal] = None
    fee_amount: Optional[Decimal] = None
    date_signed: Optional[datetime] = datetime.now()
    start_date: Optional[datetime] = datetime.now()
    end_date: Optional[datetime] = datetime.now()
    contract_info: Optional[List[UnderContractSchema] | UnderContractSchema] = None
    utilities: Optional[List[EntityBillableCreate] | EntityBillableCreate] = None

    class Config:
        from_attributes = True


class ContractResponse(BaseModel):
    """
    Schema for representing a contract response.

    Attributes:
        contract_id (Optional[UUID]): The unique identifier for the contract.
        contract_number (Optional[str]): The number of the contract (max length 128).
        contract_type (Optional[str]): The type of the contract (max length 128).
        payment_type (Optional[str]): The type of payment for the contract (max length 128).
        contract_status (str): The status of the contract (max length 128).
        contract_details (Optional[str]): The details of the contract (max length 128).
        num_invoices (Optional[int]): The number of invoices for the contract.
        payment_amount (float): The payment amount for the contract.
        fee_percentage (float): The fee percentage for the contract.
        fee_amount (float): The fee amount for the contract.
        date_signed (datetime): The date the contract was signed.
        start_date (Optional[datetime]): The start date of the contract.
        end_date (Optional[datetime]): The end date of the contract.
        contract_info (Optional[List[UnderContractSchema]]): The information of the under-contract relationships.
        utilities (Optional[List[Any]]): The utilities associated with the contract.
    """
    contract_id: Optional[UUID] = None
    contract_number: Optional[Annotated[str, constr(max_length=128)]] = None
    contract_type: Optional[Annotated[str, constr(max_length=128)]] = None
    payment_type: Optional[Annotated[str, constr(max_length=128)]] = None
    contract_status: Annotated[str, constr(max_length=128)]
    contract_details: Optional[Annotated[str, constr(max_length=128)]] = None
    num_invoices: Optional[int] = None
    payment_amount: float
    fee_percentage: float
    fee_amount: float
    date_signed: datetime = datetime.now()
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    contract_info: Optional[List[UnderContractSchema]] = None
    utilities: Optional[List[Any]] = None

    @classmethod
    def get_property_info(cls, property: Property):
        """
        Get property information.

        Args:
            property (Property): Property object.

        Returns:
            Property: Property object.
        """
        return Property(
            property_unit_assoc_id=property.property_unit_assoc_id,
            name=property.name,
            property_type=property.property_type.name,
            amount=property.amount,
            security_deposit=property.security_deposit,
            commission=property.commission,
            floor_space=property.floor_space,
            num_units=property.num_units,
            num_bathrooms=property.num_bathrooms,
            num_garages=property.num_garages,
            has_balconies=property.has_balconies,
            has_parking_space=property.has_parking_space,
            pets_allowed=property.pets_allowed,
            description=property.description,
            property_status=property.property_status,
        )

    @classmethod
    def get_property_unit_info(cls, property_unit: PropertyUnit):
        """
        Get property unit information.

        Args:
            property_unit (PropertyUnit): Property unit object.

        Returns:
            PropertyUnit: Property unit object.
        """
        return PropertyUnit(
            property_unit_assoc_id=property_unit.property_unit_assoc_id,
            property_unit_code=property_unit.property_unit_code,
            property_unit_floor_space=property_unit.property_unit_floor_space,
            property_unit_amount=property_unit.property_unit_amount,
            property_floor_id=property_unit.property_floor_id,
            property_unit_notes=property_unit.property_unit_notes,
            has_amenities=property_unit.has_amenities,
            property_id=property_unit.property_id,
            property_unit_security_deposit=property_unit.property_unit_security_deposit,
            property_unit_commission=property_unit.property_unit_commission
        )

    @classmethod
    def get_user_info(cls, user: User):
        """
        Get user information.

        Args:
            user (UserBase): User object.

        Returns:
            UserBase: User object.
        """
        return UserBase(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            gender=user.gender,
            phone_number=user.phone_number,
            photo_url=user.photo_url,
            identification_number=user.identification_number,
            date_of_birth=user.date_of_birth
        )

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
            if contract_detail.properties.property_unit_type == "Units":
                property_unit_assoc = cls.get_property_unit_info(contract_detail.properties)
            else:
                property_unit_assoc = cls.get_property_info(contract_detail.properties)

            result.append(UnderContractSchema(
                under_contract_id=contract_detail.under_contract_id,
                property_unit_assoc=property_unit_assoc,
                contract_id=contract_detail.contract_id,
                contract_status=contract_detail.contract_status,
                client_id=cls.get_user_info(contract_detail.client_representative),
                employee_id=cls.get_user_info(contract_detail.employee_representative),
            ))

        return result

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
            entity_utility : EntityBillableModel = entity_utility
            payment_type: PaymentTypeModel = entity_utility.payment_type
            utility: Utilities = entity_utility.utility

            result.append({
                "utility": utility.name,
                "frequency": payment_type.payment_type_name,
                "billable_amount": entity_utility.billable_amount,
                "apply_to_units": False,
                "entity_utilities_id": entity_utility.billable_assoc_id
            })

        return result

    @classmethod
    def from_orm_model(cls, contract: ContractModel):
        """
        Create a ContractResponse instance from an ORM model.

        Args:
            contract (ContractModel): Contract ORM model.

        Returns:
            ContractResponse: Contract response object.
        """
        return cls(
            contract_id=contract.contract_id,
            contract_number=contract.contract_number,
            contract_type=contract.contract_type_value,
            payment_type=contract.payment_type_value,
            contract_status=contract.contract_status,
            contract_details=contract.contract_details,
            num_invoices=contract.num_invoices,
            payment_amount=contract.payment_amount,
            fee_percentage=contract.fee_percentage,
            fee_amount=contract.fee_amount,
            date_signed=contract.date_signed,
            start_date=contract.start_date,
            end_date=contract.end_date,
            contract_info=cls.get_contract_details(contract.under_contract),
            utilities=cls.get_utilities_info(contract.utilities)
        ).model_dump()
