# User and Roles/Permissions/Company Associations

# role.id < user_roles.role_id
# users.user_id < user_roles.user_id
# permissions.id < role_permissions.permission_id
# role.id < role_permissions.role_id
# users.user_id < users_company.user_id
# company.company_id < users_company.company_id
# users.user_id < user_interactions.user_id
# users.user_id < documents.uploaded_by
# users.user_id < message.sender_id
# users.user_id < message_recipient.recipient_id

# Property, City, Country, and Associated Entities

# country.country_id < city.country_id  | removed this
# city.city_id < property.city_id       | changed to addresses.address_id < property.address_id 
# city.city_id < addresses.city_id 
    
# property_type.property_type_id < property.property_type_id
# property_status.property_status_id < property.property_status_id | changed this to an enum
# property.property_id < property_unit_assoc.property_id 
# units.property_unit_id < property_unit_assoc.property_unit_id
# property.property_id < units.property_id | removed this

# Utilities, Amenities, and Unit Associations

# unit_type.id < units.property_unit_type
# payment_types.payment_type_id < unit_utilities.payment_type_id
# utilities.utility_id < unit_utilities.utility_id | removed this
# amenities.amenity_id < units_amenities.amenity_id | removed this
# property_unit_assoc.property_unit_assoc < unit_utilities.property_unit_assoc | added this
# property_unit_assoc.property_unit_assoc < units_amenities.property_unit_assoc | added this

# units.property_unit_id < unit_utilities.property_unit_assoc | remove this
# units.property_unit_id < units_amenities.property_unit_assoc | remove this

# Messages and Reminders

# reminder_frequency.id < message.reminder_frequency_id
# message.message_id < message_recipient.message_id
# message.message_id < message.parent_message_id
# property_unit_assoc.property_unit_assoc < message_recipient.recipient_group_id

# Addresses and Entity Associations

# entity_address.address_id > addresses.address_id
# entity_address.entity_id > users.user_id
# entity_address.entity_id > accounts.account_id

# Contracts, Invoices, and Transactions

# contract_type.contract_type_id < contract.contract_type_id
# contract.contract_id < contract_documents.contract_id
# documents.document_number > contract_documents.document_number
# contract.contract_id < under_contract.contract_id
# contract_invoice.contract_id > contract.contract_id
# invoice.invoice_number < contract_invoice.invoice_number
# payment_types.payment_type_id < contract.payment_type_id
# transaction.transaction_id < contract.transaction_id
# transaction.transaction_id > transaction_type.transaction_type_id

# Property Assignments and Contract Associations

# property_assginment.property_type_id > property.property_id
# under_contract.property_unit_assoc > property_unit_assoc.property_unit_assoc