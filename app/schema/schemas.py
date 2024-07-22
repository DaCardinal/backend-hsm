from app.schema.base_schema import generate_schemas_for_sqlalchemy_model

from app.models.user import User
from app.models.role import Role
from app.models.permissions import Permissions
from app.models.entity_address import EntityAddress
from app.models.address import Addresses
from app.models.property import Property
from app.models.unit import Units
from app.models.message import Message
from app.models.ammenity import Amenities
from app.models.media import Media
from app.models.contract import Contract
from app.models.contract_type import ContractType
from app.models.payment_type import PaymentTypes
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.models.transaction import Transaction
from app.models.transaction_type import TransactionType
from app.models.company import Company
from app.models.maintenance_request import MaintenanceRequest
from app.models.calendar_event import CalendarEvent
from app.models.tour_bookings import Tour
from app.models.utility import Utilities
from app.models.under_contract import UnderContract
from app.models.property_assignment import PropertyAssignment


UserSchema = generate_schemas_for_sqlalchemy_model(
    User, excludes=["user_id", "password"]
)
RoleSchema = generate_schemas_for_sqlalchemy_model(Role, excludes=["role_id"])
PermissionSchema = generate_schemas_for_sqlalchemy_model(
    Permissions, excludes=["permission_id"]
)
EntityAddressSchema = generate_schemas_for_sqlalchemy_model(
    EntityAddress, excludes=["entity_assoc_id"]
)
AddressSchema = generate_schemas_for_sqlalchemy_model(
    Addresses, excludes=["address_id"]
)
PropertySchema = generate_schemas_for_sqlalchemy_model(
    Property, excludes=["property_id"]
)
PropertyUnitSchema = generate_schemas_for_sqlalchemy_model(
    Units, excludes=["property_unit_id"]
)
AmenitiesSchema = generate_schemas_for_sqlalchemy_model(
    Amenities, excludes=["amenity_id"]
)
MediaSchema = generate_schemas_for_sqlalchemy_model(Media, excludes=["media_id"])
MessageSchema = generate_schemas_for_sqlalchemy_model(Message, excludes=["message_id"])
ContractSchema = generate_schemas_for_sqlalchemy_model(
    Contract, excludes=["contract_id"]
)
ContractTypeSchema = generate_schemas_for_sqlalchemy_model(
    ContractType, excludes=["contract_type_id"]
)
PaymentTypeSchema = generate_schemas_for_sqlalchemy_model(
    PaymentTypes, excludes=["payment_type_id"]
)
InvoiceSchema = generate_schemas_for_sqlalchemy_model(
    Invoice, excludes=["invoice_number"]
)
InvoiceItemSchema = generate_schemas_for_sqlalchemy_model(
    InvoiceItem, excludes=["invoice_item_id"]
)
TransactionSchema = generate_schemas_for_sqlalchemy_model(
    Transaction, excludes=["transaction_id"]
)
TransactionTypeSchema = generate_schemas_for_sqlalchemy_model(
    TransactionType, excludes=["transaction_type_id"]
)
CompanySchema = generate_schemas_for_sqlalchemy_model(Company, excludes=["company_id"])
MaintenanceRequestSchema = generate_schemas_for_sqlalchemy_model(
    MaintenanceRequest, excludes=["task_number", "id"]
)
CalendarEventSchema = generate_schemas_for_sqlalchemy_model(
    CalendarEvent, excludes=["event_id", "id"]
)
TourBookingSchema = generate_schemas_for_sqlalchemy_model(
    Tour, excludes=["tour_booking_id"]
)
UtilitiesSchema = generate_schemas_for_sqlalchemy_model(
    Utilities, excludes=["utility_id"]
)
UnderContractSchema = generate_schemas_for_sqlalchemy_model(
    UnderContract, excludes=["under_contract_id"]
)
PropertyAssignmentSchema = generate_schemas_for_sqlalchemy_model(
    PropertyAssignment, excludes=["property_assignment_id"]
)
