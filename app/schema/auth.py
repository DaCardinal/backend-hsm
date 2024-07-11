from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional

# local imports
from app.schema.role import Role

class Token(BaseModel):
    """
    Model for representing a basic token.

    Attributes:
        access_token (str): The access token string.
        token_type (str): The type of the token, typically 'Bearer'.
    """
    access_token: str
    token_type: str

    class Config:
        from_attributes = True

class TokenExposed(BaseModel):
    """
    Model for exposing detailed token information.

    Attributes:
        user_id (Optional[UUID]): Optional user ID associated with the token.
        access_token (str): The access token string.
        token_type (str): The type of the token, typically 'Bearer'.
        first_name (str): User's first name.
        email (str): User's email.
        last_name (str): User's last name.
        expires (str): Expiration time of the token.
        roles (List[Role]): List of roles assigned to the user, defaults to an empty list.
    """
    user_id: Optional[UUID] = None
    access_token: str
    token_type: str
    first_name: str
    email: str
    last_name: str
    expires: str
    roles: List[Role] = []

    class Config():
        from_attributes = True

class TokenData(BaseModel):
    """
    Model for extracting email information from a token.

    Attributes:
        email (Optional[str]): Optional email extracted from the token.
    """
    email: Optional[str] = None

class Login(BaseModel):
    """
    Model for login request payload.

    Attributes:
        username (str): Username for login.
        password (str): Password for login.
    """
    username: str
    password: str

class ResetPassword(BaseModel):
    """
    Model for reset password request payload.

    Attributes:
        email (str): Email address to send the reset password link to.
    """
    email: str