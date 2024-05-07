from app.models import User, Role, Permissions,EntityAddress, Addresses,Property, Units, Message, Amenities, Media
from app.schema.base_schema import generate_schemas_for_sqlalchemy_model


UserSchema = generate_schemas_for_sqlalchemy_model(User, excludes=["user_id"])
RoleSchema = generate_schemas_for_sqlalchemy_model(Role, excludes=["role_id"])
PermissionSchema = generate_schemas_for_sqlalchemy_model(Permissions, excludes=["permission_id"])
EntityAddressSchema =  generate_schemas_for_sqlalchemy_model(EntityAddress, excludes=["entity_assoc_id"])
AddressSchema = generate_schemas_for_sqlalchemy_model(Addresses, excludes=['address_id'])
PropertySchema = generate_schemas_for_sqlalchemy_model(Property, excludes=['property_id'])
PropertyUnitSchema = generate_schemas_for_sqlalchemy_model(Units, excludes=['property_unit_id'])
AmmenitiesSchema = generate_schemas_for_sqlalchemy_model(Amenities, excludes=['amenity_id'])
MediaSchema = generate_schemas_for_sqlalchemy_model(Media, excludes=['media_id'])
MessageSchema = generate_schemas_for_sqlalchemy_model(Message, excludes=['message_id'])