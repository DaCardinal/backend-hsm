from app.models.user import UserModel
from app.schema.base_schema import generate_schemas_for_sqlalchemy_model

UserSchema = generate_schemas_for_sqlalchemy_model(UserModel)