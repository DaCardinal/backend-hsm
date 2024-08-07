import jwt
import bcrypt
from typing import Any
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

from app.core.config import settings

fernet = Fernet(str.encode(settings.ENCRYPT_KEY))

JWT_ALGORITHM = "HS256"


class Hash:
    def bcrypt(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

        return hashed.decode("utf-8")

    def verify(hashed_password: str, plain_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )


class SecureAccessTokens:
    def create_access_token(subject: str | Any, expires_delta: timedelta = None) -> str:
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {"exp": expire, "sub": str(subject), "type": "access"}

        return jwt.encode(
            payload=to_encode,
            key=settings.ENCRYPT_KEY,
            algorithm=JWT_ALGORITHM,
        )

    def create_refresh_token(
        subject: str | Any, expires_delta: timedelta = None
    ) -> str:
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(
                minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}

        return jwt.encode(
            payload=to_encode,
            key=settings.ENCRYPT_KEY,
            algorithm=JWT_ALGORITHM,
        )

    def decode_token(token: str) -> dict[str, Any]:
        return jwt.decode(
            jwt=token,
            key=settings.ENCRYPT_KEY,
            algorithms=[JWT_ALGORITHM],
        )

    def verify_password(
        plain_password: str | bytes, hashed_password: str | bytes
    ) -> bool:
        if isinstance(plain_password, str):
            plain_password = plain_password.encode()
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode()

        return bcrypt.checkpw(plain_password, hashed_password)

    def get_password_hash(plain_password: str | bytes) -> str:
        if isinstance(plain_password, str):
            plain_password = plain_password.encode()

        return bcrypt.hashpw(plain_password, bcrypt.gensalt()).decode()

    def get_data_encrypt(data) -> str:
        data = fernet.encrypt(data)
        return data.decode()

    def get_content(variable: str) -> str:
        return fernet.decrypt(variable.encode()).decode()
