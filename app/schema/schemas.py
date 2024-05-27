from app.models import User, Role, Permissions,EntityAddress, Addresses,Property, Units, Message, Amenities, Media, Contract, ContractType, PaymentTypes, Invoice, Transaction, TransactionType, Company, MaintenanceRequest, CalendarEvent
from app.schema.base_schema import generate_schemas_for_sqlalchemy_model


UserSchema = generate_schemas_for_sqlalchemy_model(User, excludes=["user_id", "password"])
RoleSchema = generate_schemas_for_sqlalchemy_model(Role, excludes=["role_id"])
PermissionSchema = generate_schemas_for_sqlalchemy_model(Permissions, excludes=["permission_id"])
EntityAddressSchema =  generate_schemas_for_sqlalchemy_model(EntityAddress, excludes=["entity_assoc_id"])
AddressSchema = generate_schemas_for_sqlalchemy_model(Addresses, excludes=['address_id'])
PropertySchema = generate_schemas_for_sqlalchemy_model(Property, excludes=['property_id'])
PropertyUnitSchema = generate_schemas_for_sqlalchemy_model(Units, excludes=['property_unit_id'])
AmmenitiesSchema = generate_schemas_for_sqlalchemy_model(Amenities, excludes=['amenity_id'])
MediaSchema = generate_schemas_for_sqlalchemy_model(Media, excludes=['media_id'])
MessageSchema = generate_schemas_for_sqlalchemy_model(Message, excludes=['message_id'])
ContractSchema = generate_schemas_for_sqlalchemy_model(Contract, excludes=['contract_id'])
ContractTypeSchema = generate_schemas_for_sqlalchemy_model(ContractType, excludes=['contract_type_id'])
PaymentTypeSchema = generate_schemas_for_sqlalchemy_model(PaymentTypes, excludes=['payment_type_id'])
InvoiceSchema = generate_schemas_for_sqlalchemy_model(Invoice, excludes=['invoice_number'])
TransactionSchema = generate_schemas_for_sqlalchemy_model(Transaction, excludes=['transaction_id'])
TransactionTypeSchema = generate_schemas_for_sqlalchemy_model(TransactionType, excludes=['transaction_type_id'])
CompanySchema = generate_schemas_for_sqlalchemy_model(Company, excludes=['company_id'])
MaintenanceRequestSchema = generate_schemas_for_sqlalchemy_model(MaintenanceRequest, excludes=['task_number'])
CalendarEventSchema = generate_schemas_for_sqlalchemy_model(CalendarEvent, excludes=['event_id'])