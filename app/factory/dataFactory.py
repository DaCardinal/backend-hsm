from abc import ABC, abstractmethod
from importlib import import_module
from typing import List

class DataFactory(ABC):
    @abstractmethod
    def create_data(self):
        pass

from typing import List

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

class TransactionTypeFactory:
    def __init__(self):
        models_module = import_module("app.models")
        self.model = getattr(models_module, "TransactionType")
    
    def create_data(self) -> List[dict]:
        query_key = 'transaction_type_id'

        transaction_types_data = [
            {"transaction_type_name": "Purchase"},
            {"transaction_type_name": "Sale"},
            {"transaction_type_name": "Rent"},
            {"transaction_type_name": "Lease"},
        ]
        return query_key, transaction_types_data

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

class PaymentTypesFactory:
    def __init__(self):
        models_module = import_module("app.models")
        self.model = getattr(models_module, "PaymentTypes")
    
    def create_data(self) -> List[dict]:
        query_key = 'payment_type_name'

        # payment_types_data = [
        #     {"payment_type_name": "Credit Card", "payment_type_description": "Payment via credit card"},
        #     {"payment_type_name": "Debit Card", "payment_type_description": "Payment via debit card"}
        # ]
        payment_types_data = [
            {"payment_type_name": "One-time Payment", "payment_type_description": "Payment made once"},
            {"payment_type_name": "Monthly Payment", "payment_type_description": "Payment made monthly"},
            {"payment_type_name": "Quarterly Payment", "payment_type_description": "Payment made quarterly"},
            {"payment_type_name": "Semi-annual Payment", "payment_type_description": "Payment made semi-annually"},
            {"payment_type_name": "Annual Payment", "payment_type_description": "Payment made annually"}
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