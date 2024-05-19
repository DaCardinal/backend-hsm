from abc import ABC, abstractmethod
from importlib import import_module
from typing import List
import uuid

class DataFactory(ABC):
    @abstractmethod
    def create_data(self):
        pass

class PermissionsFactory:
    def __init__(self):
        models_module = import_module("app.models")
        self.model = getattr(models_module, "Permissions")
    
    def create_data(self) -> List[dict]:
        query_key = 'alias'

        permissions_data = [
            {'name': 'view_landlord', 'description': 'Grants permission to view landlord', 'alias': 'view_landlord'},
            {'name': 'create_landlord', 'description': 'Grants permission to create new landlord', 'alias': 'create_landlord'},
            {'name': 'update_landlord', 'description': 'Grants permission to update landlord', 'alias': 'update_landlord'},
            {'name': 'delete_landlord', 'description': 'Grants permission to delete landlord', 'alias': 'delete_landlord'},
            {'name': 'view_tenant', 'description': 'Grants permission to view tenant', 'alias': 'view_tenant'},
            {'name': 'create_tenant', 'description': 'Grants permission to create new tenant', 'alias': 'create_tenant'},
            {'name': 'update_tenant', 'description': 'Grants permission to update tenant', 'alias': 'update_tenant'},
            {'name': 'delete_tenant', 'description': 'Grants permission to delete tenant', 'alias': 'delete_tenant'},
            {'name': 'view_lease_history', 'description': 'Grants permission to view lease_history', 'alias': 'view_lease_history'},
            {'name': 'create_lease_history', 'description': 'Grants permission to create new lease_history', 'alias': 'create_lease_history'},
            {'name': 'update_lease_history', 'description': 'Grants permission to update lease_history', 'alias': 'update_lease_history'},
            {'name': 'delete_lease_history', 'description': 'Grants permission to delete lease_history', 'alias': 'delete_lease_history'},
            {'name': 'view_properties', 'description': 'Grants permission to view properties', 'alias': 'view_properties'},
            {'name': 'create_properties', 'description': 'Grants permission to create new properties', 'alias': 'create_properties'},
            {'name': 'update_properties', 'description': 'Grants permission to update properties', 'alias': 'update_properties'},
            {'name': 'delete_properties', 'description': 'Grants permission to delete properties', 'alias': 'delete_properties'},
            {'name': 'view_units', 'description': 'Grants permission to view units', 'alias': 'view_units'},
            {'name': 'create_units', 'description': 'Grants permission to create new units', 'alias': 'create_units'},
            {'name': 'update_units', 'description': 'Grants permission to update units', 'alias': 'update_units'},
            {'name': 'delete_units', 'description': 'Grants permission to delete units', 'alias': 'delete_units'},
            {'name': 'view_events', 'description': 'Grants permission to view events', 'alias': 'view_events'},
            {'name': 'create_events', 'description': 'Grants permission to create new events', 'alias': 'create_events'},
            {'name': 'update_events', 'description': 'Grants permission to update events', 'alias': 'update_events'},
            {'name': 'delete_events', 'description': 'Grants permission to delete events', 'alias': 'delete_events'},
            {'name': 'view_leases', 'description': 'Grants permission to view leases', 'alias': 'view_leases'},
            {'name': 'create_leases', 'description': 'Grants permission to create new leases', 'alias': 'create_leases'},
            {'name': 'update_leases', 'description': 'Grants permission to update leases', 'alias': 'update_leases'},
            {'name': 'delete_leases', 'description': 'Grants permission to delete leases', 'alias': 'delete_leases'},
            {'name': 'view_users', 'description': 'Grants permission to view users', 'alias': 'view_users'},
            {'name': 'create_users', 'description': 'Grants permission to create new users', 'alias': 'create_users'},
            {'name': 'update_users', 'description': 'Grants permission to update users', 'alias': 'update_users'},
            {'name': 'delete_users', 'description': 'Grants permission to delete users', 'alias': 'delete_users'},
            {'name': 'view_invoice', 'description': 'Grants permission to view invoice', 'alias': 'view_invoice'},
            {'name': 'create_invoice', 'description': 'Grants permission to create new invoice', 'alias': 'create_invoice'},
            {'name': 'update_invoice', 'description': 'Grants permission to update invoice', 'alias': 'update_invoice'},
            {'name': 'delete_invoice', 'description': 'Grants permission to delete invoice', 'alias': 'delete_invoice'}
        ]


        return query_key, permissions_data

class RolesFactory:
    def __init__(self):
        models_module = import_module("app.models")
        self.model = getattr(models_module, "Role")
    
    def create_data(self) -> List[dict]:
        query_key = 'alias'

        roles_data = [
            {
                "name": "admin",
                "alias": "admin",
                "description": "Role for admin user priveleges"
            },
            {
                "name": "tenant",
                "alias": "tenant",
                "description": "Role for tenant user priveleges"
            },
            {
                "name": "landlord",
                "alias": "landlord",
                "description": "Role for landlord user priveleges"
            }
        ]

        return query_key, roles_data
    
class RolePermissionsFactory:
    def __init__(self):
        models_module = import_module("app.models")
        self.model = getattr(models_module, "RolePermissions")
    
    def create_data(self) -> List[dict]:
        query_key = 'role_permissions'

        admin_permissions_data = [
        {
            "name": "view_landlord",
            "description": "Grants permission to view landlord",
            "alias": "view_landlord"
        },
        {
            "name": "create_landlord",
            "description": "Grants permission to create new landlord",
            "alias": "create_landlord"
        },
        {
            "name": "update_landlord",
            "description": "Grants permission to update landlord",
            "alias": "update_landlord"
        },
        {
            "name": "delete_landlord",
            "description": "Grants permission to delete landlord",
            "alias": "delete_landlord"
        },
        {
            "name": "view_tenant",
            "description": "Grants permission to view tenant",
            "alias": "view_tenant"
        },
        {
            "name": "create_tenant",
            "description": "Grants permission to create new tenant",
            "alias": "create_tenant"
        },
        {
            "name": "update_tenant",
            "description": "Grants permission to update tenant",
            "alias": "update_tenant"
        },
        {
            "name": "delete_tenant",
            "description": "Grants permission to delete tenant",
            "alias": "delete_tenant"
        },
        {
            "name": "view_lease_history",
            "description": "Grants permission to view lease_history",
            "alias": "view_lease_history"
        },
        {
            "name": "create_lease_history",
            "description": "Grants permission to create new lease_history",
            "alias": "create_lease_history"
        },
        {
            "name": "update_lease_history",
            "description": "Grants permission to update lease_history",
            "alias": "update_lease_history"
        },
        {
            "name": "delete_lease_history",
            "description": "Grants permission to delete lease_history",
            "alias": "delete_lease_history"
        },
        {
            "name": "view_properties",
            "description": "Grants permission to view properties",
            "alias": "view_properties"
        },
        {
            "name": "create_properties",
            "description": "Grants permission to create new properties",
            "alias": "create_properties"
        },
        {
            "name": "update_properties",
            "description": "Grants permission to update properties",
            "alias": "update_properties"
        },
        {
            "name": "delete_properties",
            "description": "Grants permission to delete properties",
            "alias": "delete_properties"
        },
        {
            "name": "view_units",
            "description": "Grants permission to view units",
            "alias": "view_units"
        },
        {
            "name": "create_units",
            "description": "Grants permission to create new units",
            "alias": "create_units"
        },
        {
            "name": "update_units",
            "description": "Grants permission to update units",
            "alias": "update_units"
        },
        {
            "name": "delete_units",
            "description": "Grants permission to delete units",
            "alias": "delete_units"
        },
        {
            "name": "view_events",
            "description": "Grants permission to view events",
            "alias": "view_events"
        },
        {
            "name": "create_events",
            "description": "Grants permission to create new events",
            "alias": "create_events"
        },
        {
            "name": "update_events",
            "description": "Grants permission to update events",
            "alias": "update_events"
        },
        {
            "name": "delete_events",
            "description": "Grants permission to delete events",
            "alias": "delete_events"
        },
        {
            "name": "view_leases",
            "description": "Grants permission to view leases",
            "alias": "view_leases"
        },
        {
            "name": "create_leases",
            "description": "Grants permission to create new leases",
            "alias": "create_leases"
        },
        {
            "name": "update_leases",
            "description": "Grants permission to update leases",
            "alias": "update_leases"
        },
        {
            "name": "delete_leases",
            "description": "Grants permission to delete leases",
            "alias": "delete_leases"
        },
        {
            "name": "view_users",
            "description": "Grants permission to view users",
            "alias": "view_users"
        },
        {
            "name": "create_users",
            "description": "Grants permission to create new users",
            "alias": "create_users"
        },
        {
            "name": "update_users",
            "description": "Grants permission to update users",
            "alias": "update_users"
        },
        {
            "name": "delete_users",
            "description": "Grants permission to delete users",
            "alias": "delete_users"
        },
        {
            "name": "view_invoice",
            "description": "Grants permission to view invoice",
            "alias": "view_invoice"
        },
        {
            "name": "create_invoice",
            "description": "Grants permission to create new invoice",
            "alias": "create_invoice"
        },
        {
            "name": "update_invoice",
            "description": "Grants permission to update invoice",
            "alias": "update_invoice"
        },
        {
            "name": "delete_invoice",
            "description": "Grants permission to delete invoice",
            "alias": "delete_invoice"
        }
    ]

        tenant_permissions_data = [
        {
            "name": "view_events",
            "description": "Grants permission to view events",
            "alias": "view_events"
        },
        {
            "name": "create_events",
            "description": "Grants permission to create new events",
            "alias": "create_events"
        },
        {
            "name": "update_events",
            "description": "Grants permission to update events",
            "alias": "update_events"
        },
        {
            "name": "delete_events",
            "description": "Grants permission to delete events",
            "alias": "delete_events"
        }
    ]

        landlord_permissions_data = [
        {
            "name": "view_tenant",
            "description": "Grants permission to view tenant",
            "alias": "view_tenant"
        },
        {
            "name": "create_tenant",
            "description": "Grants permission to create new tenant",
            "alias": "create_tenant"
        },
        {
            "name": "update_tenant",
            "description": "Grants permission to update tenant",
            "alias": "update_tenant"
        },
        {
            "name": "delete_tenant",
            "description": "Grants permission to delete tenant",
            "alias": "delete_tenant"
        },
        {
            "name": "view_lease_history",
            "description": "Grants permission to view lease_history",
            "alias": "view_lease_history"
        },
        {
            "name": "create_lease_history",
            "description": "Grants permission to create new lease_history",
            "alias": "create_lease_history"
        },
        {
            "name": "update_lease_history",
            "description": "Grants permission to update lease_history",
            "alias": "update_lease_history"
        },
        {
            "name": "delete_lease_history",
            "description": "Grants permission to delete lease_history",
            "alias": "delete_lease_history"
        },
        {
            "name": "view_properties",
            "description": "Grants permission to view properties",
            "alias": "view_properties"
        },
        {
            "name": "create_properties",
            "description": "Grants permission to create new properties",
            "alias": "create_properties"
        },
        {
            "name": "update_properties",
            "description": "Grants permission to update properties",
            "alias": "update_properties"
        },
        {
            "name": "delete_properties",
            "description": "Grants permission to delete properties",
            "alias": "delete_properties"
        },
        {
            "name": "view_units",
            "description": "Grants permission to view units",
            "alias": "view_units"
        },
        {
            "name": "create_units",
            "description": "Grants permission to create new units",
            "alias": "create_units"
        },
        {
            "name": "update_units",
            "description": "Grants permission to update units",
            "alias": "update_units"
        },
        {
            "name": "delete_units",
            "description": "Grants permission to delete units",
            "alias": "delete_units"
        },
        {
            "name": "view_events",
            "description": "Grants permission to view events",
            "alias": "view_events"
        },
        {
            "name": "create_events",
            "description": "Grants permission to create new events",
            "alias": "create_events"
        },
        {
            "name": "update_events",
            "description": "Grants permission to update events",
            "alias": "update_events"
        },
        {
            "name": "delete_events",
            "description": "Grants permission to delete events",
            "alias": "delete_events"
        },
        {
            "name": "view_leases",
            "description": "Grants permission to view leases",
            "alias": "view_leases"
        },
        {
            "name": "create_leases",
            "description": "Grants permission to create new leases",
            "alias": "create_leases"
        },
        {
            "name": "update_leases",
            "description": "Grants permission to update leases",
            "alias": "update_leases"
        },
        {
            "name": "delete_leases",
            "description": "Grants permission to delete leases",
            "alias": "delete_leases"
        },
        {
            "name": "view_invoice",
            "description": "Grants permission to view invoice",
            "alias": "view_invoice"
        },
        {
            "name": "create_invoice",
            "description": "Grants permission to create new invoice",
            "alias": "create_invoice"
        },
        {
            "name": "update_invoice",
            "description": "Grants permission to update invoice",
            "alias": "update_invoice"
        },
        {
            "name": "delete_invoice",
            "description": "Grants permission to delete invoice",
            "alias": "delete_invoice"
        }
    ]

        
        role_permissions_data = [
            {
                "name": "admin",
                "description": "Role for admin user priveleges",
                "permissions": admin_permissions_data
            },
            {
                "name": "tenant",
                "description": "Role for tenant user priveleges",
                "permissions": tenant_permissions_data
            },
            {
                "name": "landlord",
                "description": "Role for landlord user priveleges",
                "permissions": landlord_permissions_data
            }
        ]

        return query_key, role_permissions_data

class UserFactory:
    def __init__(self):
        models_module = import_module("app.models")
        self.model = getattr(models_module, "User")
    
    def create_data(self) -> List[dict]:
        query_key = 'email'

        user_data = [
            {
                "user_id": uuid.UUID("0d5340d2-046b-42d9-9ef5-0233b79b6642"),
                "first_name": "John",
                "last_name": "Doe",
                "email": "admin@housekee.com",
                "date_of_birth": "1989-07-19",
                "phone_number": "59123456789",
                "password": "$2b$12$vVs/j4HpV4j4Mb7PHAKOZe3C1dsMthIaHyM2Oh2.wXE2oG9I6KLHi",
                "identification_number": "string",
                "photo_url": "string",
                "gender": "male"
            },
            {
                "user_id": uuid.UUID("4dbc3019-1884-4a0d-a2e6-feb12d83186e"),
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "tenant@housekee.com",
                "date_of_birth": "1989-07-19",
                "phone_number": "59123456789",
                "password": "$2b$12$vVs/j4HpV4j4Mb7PHAKOZe3C1dsMthIaHyM2Oh2.wXE2oG9I6KLHi",
                "identification_number": "GHA-0987654321",
                "photo_url": "string",
                "gender": "male"
            },
            {
                "user_id": uuid.UUID("889fabef-e15b-4aea-8538-5206b8b8a579"),
                "first_name": "Jackson",
                "last_name": "Doe",
                "email": "landlord@housekee.com",
                "date_of_birth": "1989-07-19",
                "phone_number": "59123456789",
                "password": "$2b$12$vVs/j4HpV4j4Mb7PHAKOZe3C1dsMthIaHyM2Oh2.wXE2oG9I6KLHi",
                "identification_number": "GHA-1234567890",
                "photo_url": "string",
                "gender": "male"
            }
        ]

        return query_key, user_data

class MediaFactory:
    def __init__(self):
        models_module = import_module("app.models")
        self.model = getattr(models_module, "Media")
    
    def create_data(self) -> List[dict]:
        query_key = 'media_name'

        media_data = [
            {"media_name": "Image 1", "media_type": "image", "content_url": "https://media.istockphoto.com/id/1492279317/photo/moments-in-the-river.jpg?s=1024x1024&w=is&k=20&c=EPKDRGX38EKB1fQO7GFYrFAMs2cejE4IYk6b3i0VCVk="},
            {"media_name": "Image 2", "media_type": "image", "content_url": "https://media.istockphoto.com/id/1492279317/photo/moments-in-the-river.jpg?s=1024x1024&w=is&k=20&c=EPKDRGX38EKB1fQO7GFYrFAMs2cejE4IYk6b3i0VCVk="},
            {"media_name": "Image 3", "media_type": "image", "content_url": "https://media.istockphoto.com/id/1492279317/photo/moments-in-the-river.jpg?s=1024x1024&w=is&k=20&c=EPKDRGX38EKB1fQO7GFYrFAMs2cejE4IYk6b3i0VCVk="}
        ]
        return query_key, media_data

class CountryFactory:
    def __init__(self):
        models_module = import_module("app.models")
        self.model = getattr(models_module, "Country")
    
    def create_data(self) -> List[dict]:
        query_key = 'country_name'

        countries = [
            "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", 
            "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", 
            "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", 
            "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", 
            "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", 
            "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", 
            "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", 
            "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", 
            "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", 
            "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", 
            "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", 
            "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North", 
            "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", 
            "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", 
            "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", 
            "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", 
            "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", 
            "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", 
            "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", 
            "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", 
            "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", 
            "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", 
            "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", 
            "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", 
            "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", 
            "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", 
            "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", 
            "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", 
            "Yemen", "Zambia", "Zimbabwe"
        ]
        
        country_data = [{"country_name": country} for country in countries]
        return query_key, country_data
    
class UnitTypeFactory:
    def __init__(self):
        models_module = import_module("app.models")
        self.model = getattr(models_module, "PropertyType")
    
    def create_data(self) -> List[dict]:
        query_key = 'name'

        unit_types_data = [
            {"unit_type_name": "Studio"},
            {"unit_type_name": "One Bedroom"},
            {"unit_type_name": "Two Bedroom"},
            {"unit_type_name": "Three Bedroom"}
        ]
        return query_key, unit_types_data

class PropertyTypeFactory:
    def __init__(self):
        models_module = import_module("app.models")
        self.model = getattr(models_module, "PropertyType")
    
    def create_data(self) -> List[dict]:
        query_key = 'name'

        property_types_data = [
            {"name": "House", "description": "A standalone residential building"},
            {"name": "Apartment", "description": "A residential unit within a larger building"},
            {"name": "Condominium", "description": "A privately owned individual unit within a larger complex"},
            {"name": "Townhouse", "description": "A narrow, multi-story attached home with shared walls"},
            {"name": "Duplex", "description": "A residential building with two separate living units"},
            {"name": "Villa", "description": "A luxurious standalone residence often found in resort areas"},
            {"name": "Bungalow", "description": "A single-story house with a low-pitched roof and wide verandas"},
            {"name": "Penthouse", "description": "An apartment or unit on the top floor of a building"}
        ]
        return query_key, property_types_data

class TransactionTypeFactory:
    def __init__(self) -> None:
        models_module = import_module("app.models")
        self.model = getattr(models_module, "TransactionType")

    def create_data(self) -> List[dict]:
        query_key = "transaction_type_name"
        
        transaction_type_data = [
            {"transaction_type_name": "credit_card", "transaction_type_description": "Payment via credit card"},
            {"transaction_type_name": "debit_card", "transaction_type_description": "Payment via debit card"},
            {"transaction_type_name": "mobile_money", "transaction_type_description": "Payment via mobile money"}
        ]

        return query_key, transaction_type_data

class ContractTypeFactory:
    def __init__(self):
        models_module = import_module("app.models")
        self.model = getattr(models_module, "ContractType")
    
    def create_data(self) -> List[dict]:
        query_key = 'contract_type_name'

        contract_type_data = [
            {"contract_type_name": "purchase", "fee_percentage": 10.00},
            {"contract_type_name": "sale", "fee_percentage": 5.10},
            {"contract_type_name": "rent",  "fee_percentage": 14.5},
            {"contract_type_name": "lease",  "fee_percentage": 3.25},
        ]

        return query_key, contract_type_data

class PaymentTypesFactory:
    def __init__(self):
        models_module = import_module("app.models")
        self.model = getattr(models_module, "PaymentTypes")
    
    def create_data(self) -> List[dict]:
        query_key = 'payment_type_name'

        # payment_types_data = [
        #     {"payment_type_name": "One-time Payment", "payment_type_description": "Payment made once", "num_of_invoices": 1},
        #     {"payment_type_name": "Monthly Payment", "payment_type_description": "Payment made monthly", "num_of_invoices": 12},
        #     {"payment_type_name": "Quarterly Payment", "payment_type_description": "Payment made quarterly", "num_of_invoices": 4},
        #     {"payment_type_name": "Semi-annual Payment", "payment_type_description": "Payment made semi-annually", "num_of_invoices": 2},
        #     {"payment_type_name": "Annual Payment", "payment_type_description": "Payment made annually", "num_of_invoices": 1}
        # ]
        payment_types_data = [
            {"payment_type_name": "one-time", "payment_type_description": "Payment made once", "num_of_invoices": 1},
            {"payment_type_name": "monthly", "payment_type_description": "Payment made monthly", "num_of_invoices": 12},
            {"payment_type_name": "quarterly", "payment_type_description": "Payment made quarterly", "num_of_invoices": 4},
            {"payment_type_name": "semi-annual", "payment_type_description": "Payment made semi-annually", "num_of_invoices": 2},
            {"payment_type_name": "annual", "payment_type_description": "Payment made annually", "num_of_invoices": 1}
        ]
        return query_key, payment_types_data

class UtilitiesFactory:
    def __init__(self):
        models_module = import_module("app.models")
        self.model = getattr(models_module, "Utilities")
    
    def create_data(self) -> List[dict]:
        query_key = 'name'

        utilities_data = [
            {"name": "Electricity", "description": "Utility for providing electrical power"},
            {"name": "Water", "description": "Utility for providing water supply"}
        ]
        return query_key, utilities_data

class AmmenityFactory(DataFactory):
    def __init__(self):
        models_module = import_module("app.models")
        self.model = getattr(models_module, "Amenities")

    def create_data(self):
        query_key = 'amenity_name'

        default_items = [
            {
                "amenity_name": "Swimming Pool",
                "amenity_short_name": "Pool",
                "amenity_value_type": "boolean",
                "description": "A pool for swimming and recreation",
            },
            {
                "amenity_name": "Gym",
                "amenity_short_name": "Gym",
                "amenity_value_type": "boolean",
                "description": "A facility equipped for physical exercise",
            },
            {
                "amenity_name": "Parking",
                "amenity_short_name": "Parking",
                "amenity_value_type": "boolean",
                "description": "Designated area for parking vehicles",
            },
            {
                "amenity_name": "Playground",
                "amenity_short_name": "Playground",
                "amenity_value_type": "boolean",
                "description": "An outdoor area equipped for children's play",
            },
            {
                "amenity_name": "Clubhouse",
                "amenity_short_name": "Clubhouse",
                "amenity_value_type": "boolean",
                "description": "A social club or community building",
            },
            {
                "amenity_name": "Security",
                "amenity_short_name": "Security",
                "amenity_value_type": "boolean",
                "description": "Security measures or personnel for safety",
            },
            {
                "amenity_name": "Pets Allowed",
                "amenity_short_name": "Pets",
                "amenity_value_type": "boolean",
                "description": "Pets are permitted on the property",
            },
            {
                "amenity_name": "Balcony",
                "amenity_short_name": "Balcony",
                "amenity_value_type": "boolean",
                "description": "An outdoor platform extending from a building",
            },
            {
                "amenity_name": "Fireplace",
                "amenity_short_name": "Fireplace",
                "amenity_value_type": "boolean",
                "description": "A structure for containing a fire",
            },
            {
                "amenity_name": "Laundry Facilities",
                "amenity_short_name": "Laundry",
                "amenity_value_type": "boolean",
                "description": "Facilities for washing and drying clothes",
            }
        ]
        return query_key, default_items