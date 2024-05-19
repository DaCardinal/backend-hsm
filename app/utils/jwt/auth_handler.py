import time
import jwt
from typing import Dict

from app.models import User
from app.utils import settings
from app.schema import TokenExposed, UserBase

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM


def token_response(token: str) -> TokenExposed:
    payload = decodeJWT(token)
    payload.update({"access_token": token, "token_type": "Bearer"})
    
    return payload

def signJWT(user: User) -> Dict[str, str]:
    
    payload = user.to_dict(exclude={'password_hash', 'updated_at', 'created_at', 'gender', 'user_id'})
    payload = {key: payload[key] for key in payload if key in UserBase.model_fields}
    payload.update({"expires": time.time() + 1800})

    # create the access token with the user's scopes as permissions
    user_permissions = [p.name for r in user.roles for p in r.permissions]
    payload.update({"scope": ','.join(user_permissions)})
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    token_data = token_response(token)
    token_data.update({
        "first_name": user.first_name,
        "email": user.email,
        "user_id": user.to_dict().get('user_id'),
        "last_name": user.last_name,
        "expires": payload["expires"],
        "roles": user.roles
    })

    return token_data

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}