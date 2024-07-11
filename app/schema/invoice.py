from uuid import UUID
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, constr
from typing import Any, List, Optional, Union, Annotated

from app.schema.user import UserBase
from app.schema.enums import PaymentStatus
from app.schema.property import Property, PropertyUnit, PropertyBase, PropertyUnitBase

from app.models import Invoice as InvoiceModel, Contract as ContractModel
from app.models.property_unit_assoc import PropertyUnitAssoc as PropertyUnitAssocModel

# TODO: Check naming of `InvoiceItemUpdate` to `InvoiceItemUpdateSchema`

class InvoiceItemBase(BaseModel):
    """
    Base model for invoice item information.

    Attributes:
        quantity (int): The quantity of the invoice item.
        unit_price (Decimal): The unit price of the invoice item.
        total_price (Decimal): The total price of the invoice item.
        reference_id (Optional[str]): The reference ID for the invoice item.
        description (Optional[str]): The description of the invoice item.
    """
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    reference_id: Optional[Annotated[str, constr(max_length=255)]] = None
    description: Optional[Annotated[str, constr(max_length=255)]] = None

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class InvoiceItem(BaseModel):
    """
    Model for representing an invoice item with additional details.

    Attributes:
        quantity (int): The quantity of the invoice item.
        unit_price (Decimal): The unit price of the invoice item.
        total_price (Decimal): The total price of the invoice item.
        invoice_item_id (UUID): The unique identifier for the invoice item.
        invoice_number (UUID): The unique identifier for the invoice.
        reference_id (Optional[str]): The reference ID for the invoice item.
        description (Optional[str]): The description of the invoice item.
    """
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    invoice_item_id: UUID
    invoice_number: UUID
    reference_id: Optional[Annotated[str, constr(max_length=255)]] = None
    description: Optional[Annotated[str, constr(max_length=255)]] = None

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class InvoiceItemUpdate(InvoiceItemBase):
    """
    Schema for updating an invoice item.

    Attributes:
        invoice_item_id (Optional[UUID]): The unique identifier for the invoice item.
    """
    invoice_item_id: Optional[UUID] = None

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class InvoiceItemCreateSchema(InvoiceItemBase):
    """
    Schema for creating an invoice item.

    Inherits from InvoiceItemBase.
    """
    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class InvoiceBase(BaseModel):
    """
    Base model for invoice information.

    Attributes:
        issued_by (Optional[UUID | UserBase]): The issuer of the invoice.
        issued_to (Optional[UUID | UserBase]): The recipient of the invoice.
        invoice_details (Optional[str]): The details of the invoice.
        due_date (Optional[datetime]): The due date of the invoice.
        date_paid (Optional[datetime]): The date the invoice was paid.
        status (PaymentStatusEnum | str): The status of the payment.
        transaction_id (Optional[UUID]): The transaction ID for the payment.
        invoice_items (List[InvoiceItemBase]): The items in the invoice.
    """
    issued_by: Optional[Union[UUID, UserBase]] = None
    issued_to: Optional[Union[UUID, UserBase]] = None
    invoice_details: Optional[Annotated[str, constr(max_length=255)]] = None
    due_date: Optional[datetime] = None
    date_paid: Optional[datetime] = None
    status: Union[PaymentStatus, Annotated[str, constr(max_length=50)]]
    transaction_id: Optional[UUID] = None
    invoice_items: List[InvoiceItemBase] = []

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class Invoice(BaseModel):
    """
    Base model for invoice information.

    Attributes:
        invoice_number (Optional[str]): The number of the invoice.
        issued_by (Optional[UUID | UserBase]): The issuer of the invoice.
        issued_to (Optional[UUID | UserBase]): The recipient of the invoice.
        invoice_details (Optional[str]): The details of the invoice.
        due_date (Optional[datetime]): The due date of the invoice.
        date_paid (Optional[datetime]): The date the invoice was paid.
        status (PaymentStatusEnum | str): The status of the payment.
        transaction_id (Optional[UUID]): The transaction ID for the payment.
        invoice_items (List[InvoiceItemBase]): The items in the invoice.
    """
    invoice_number: Optional[str]
    issued_by: Optional[Union[UUID, UserBase]] = None
    issued_to: Optional[Union[UUID, UserBase]] = None
    invoice_details: Optional[Annotated[str, constr(max_length=255)]] = None
    due_date: Optional[datetime] = None
    date_paid: Optional[datetime] = None
    status: Union[PaymentStatus, Annotated[str, constr(max_length=50)]]
    transaction_id: Optional[UUID] = None
    invoice_items: List[InvoiceItemBase] = []

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class InvoiceCreateSchema(InvoiceBase):
    """
    Schema for creating an invoice.

    Inherits from InvoiceBase.
    """
    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class InvoiceUpdateSchema(InvoiceBase):
    """
    Schema for updating an invoice.

    Attributes:
        id (Optional[UUID]): The unique identifier for the invoice.
        invoice_number (Optional[str]): The number of the invoice.
    """
    id: Optional[UUID] = None
    invoice_number: Optional[Annotated[str, constr(max_length=50)]] = None

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class InvoiceResponse(BaseModel):
    """
    Model for representing an invoice response.

    Attributes:
        id (Optional[UUID]): The unique identifier for the invoice.
        invoice_number (Optional[str]): The number of the invoice.
        issued_by (Optional[UUID | UserBase]): The issuer of the invoice.
        issued_to (Optional[UUID | UserBase]): The recipient of the invoice.
        invoice_details (Optional[str]): The details of the invoice.
        invoice_amount (Decimal): The total amount of the invoice.
        due_date (Optional[datetime]): The due date of the invoice.
        date_paid (Optional[datetime]): The date the invoice was paid.
        status (PaymentStatusEnum): The status of the payment.
        transaction_id (Optional[UUID]): The transaction ID for the payment.
        invoice_items (List[InvoiceItemBase]): The items in the invoice.
    """
    id: Optional[UUID] = None
    invoice_number: Optional[Annotated[str, constr(max_length=50)]] = None
    issued_by: Optional[Union[UUID, UserBase]] = None
    issued_to: Optional[Union[UUID, UserBase]] = None
    invoice_details: Optional[Annotated[str, constr(max_length=255)]] = None
    invoice_amount: Decimal
    due_date: Optional[datetime] = None
    date_paid: Optional[datetime] = None
    status: PaymentStatus
    transaction_id: Optional[UUID] = None
    invoice_items: List[InvoiceItemBase] = []

    @classmethod
    def get_invoice_items(cls, invoice_details: List[InvoiceItem]) -> List[InvoiceItemBase]:
        """
        Get the items in the invoice.

        Args:
            invoice_details (List[InvoiceItem]): List of invoice items.

        Returns:
            List[InvoiceItemBase]: List of invoice item base objects.
        """
        result = []
        for invoice in invoice_details:
            result.append(InvoiceItemBase(
                reference_id=invoice.reference_id,
                description=invoice.description,
                quantity=invoice.quantity,
                unit_price=invoice.unit_price,
                total_price=invoice.total_price
            ))
        return result

    @classmethod
    def from_orm_model(cls, invoice: InvoiceModel) -> 'InvoiceResponse':
        """
        Create an InvoiceResponse instance from an ORM model.

        Args:
            invoice (InvoiceModel): Invoice ORM model.

        Returns:
            InvoiceResponse: Invoice response object.
        """
        return cls(
            id=invoice.id,
            invoice_number=invoice.invoice_number,
            issued_by=invoice.issued_by_user,
            issued_to=invoice.issued_to_user,
            invoice_details=invoice.invoice_details,
            invoice_amount=invoice.invoice_amount,
            due_date=invoice.due_date,
            date_paid=invoice.date_paid,
            status=invoice.status,
            transaction_id=invoice.transaction_id,
            invoice_items=cls.get_invoice_items(invoice.invoice_items)
        ).model_dump()


class InvoiceDueResponse(BaseModel):
    """
    Model for representing an invoice due response.

    Attributes:
        id (Optional[UUID]): The unique identifier for the invoice.
        invoice_number (Optional[str]): The number of the invoice.
        issued_by (Optional[UUID | UserBase]): The issuer of the invoice.
        issued_to (Optional[UUID | UserBase]): The recipient of the invoice.
        invoice_details (Optional[str]): The details of the invoice.
        invoice_amount (Decimal): The total amount of the invoice.
        due_date (Optional[datetime]): The due date of the invoice.
        date_paid (Optional[datetime]): The date the invoice was paid.
        status (PaymentStatusEnum): The status of the payment.
        transaction_id (Optional[UUID]): The transaction ID for the payment.
        invoice_items (List[InvoiceItemBase]): The items in the invoice.
    """
    id: Optional[UUID] = None
    invoice_number: Optional[Annotated[str, constr(max_length=50)]] = None
    issued_by: Optional[Union[UUID, UserBase]] = None
    issued_to: Optional[Union[UUID, UserBase]] = None
    invoice_details: Optional[Annotated[str, constr(max_length=255)]] = None
    invoice_amount: Decimal
    due_date: Optional[datetime] = None
    date_paid: Optional[datetime] = None
    status: PaymentStatus
    transaction_id: Optional[UUID] = None
    invoice_items: List[InvoiceItemBase] = []
    property: Optional[List[Union[Property, PropertyUnit]]]

    @classmethod
    def get_invoice_items(cls, invoice_details: List[InvoiceItem]) -> List[InvoiceItemBase]:
        """
        Get the items in the invoice.

        Args:
            invoice_details (List[InvoiceItem]): List of invoice items.

        Returns:
            List[InvoiceItemBase]: List of invoice item base objects.
        """
        result = []
        for invoice in invoice_details:
            result.append(InvoiceItemBase(
                reference_id=invoice.reference_id,
                description=invoice.description,
                quantity=invoice.quantity,
                unit_price=invoice.unit_price,
                total_price=invoice.total_price
            ))
        return result
    
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
            property_status=property.property_status
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
    def get_property_details(cls, contract_details: List[ContractModel]):
        """
        Extract and format property details from a list of contract models.

        This method iterates over the provided contract models, extracting and converting
        property unit associations to their corresponding details based on their type (either
        'Units' or other types).

        Args:
            contract_details (List[ContractModel]): A list of contract models from which property
            details are extracted.
        """
        result = []

        for contract in contract_details:
            property_unit_assoc_details : List[PropertyUnitAssocModel] = contract.properties

            for property_unit_assoc in property_unit_assoc_details:
                if property_unit_assoc.property_unit_type == "Units":
                    property_unit_assoc = cls.get_property_unit_info(property_unit_assoc)
                else:
                    property_unit_assoc = cls.get_property_info(property_unit_assoc)
                result.append(property_unit_assoc)
        
        return result

    @classmethod
    def from_orm_model(cls, invoice: InvoiceModel) -> 'InvoiceResponse':
        """
        Create an InvoiceDueResponse instance from an ORM model.

        Args:
            invoice (InvoiceModel): Invoice ORM model.

        Returns:
            InvoiceResponse: Invoice response object.
        """
        return cls(
            id=invoice.id,
            invoice_number=invoice.invoice_number,
            issued_by=invoice.issued_by_user,
            issued_to=invoice.issued_to_user,
            invoice_details=invoice.invoice_details,
            invoice_amount=invoice.invoice_amount,
            due_date=invoice.due_date,
            date_paid=invoice.date_paid,
            status=invoice.status,
            transaction_id=invoice.transaction_id,
            invoice_items=cls.get_invoice_items(invoice.invoice_items),
            property=cls.get_property_details(invoice.contracts)
        ).model_dump()
