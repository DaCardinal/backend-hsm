from app.models import User, Role, Permissions
from app.schema.base_schema import generate_schemas_for_sqlalchemy_model

UserSchema = generate_schemas_for_sqlalchemy_model(User, excludes=["user_id"])
RoleSchema = generate_schemas_for_sqlalchemy_model(Role, excludes=["role_id"])
PermissionSchema = generate_schemas_for_sqlalchemy_model(Permissions, excludes=["permission_id"])