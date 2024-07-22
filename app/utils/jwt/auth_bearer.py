from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# utils
from app.utils.jwt.auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, scopes: list = [], auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.scopes = scopes

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )

            payload = self.verify_jwt(credentials.credentials)
            if not payload:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )

            token_scopes = payload["scope"].split(",")
            if self.scopes and not any(scope in token_scopes for scope in self.scopes):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return credentials.credentials

    def verify_jwt(self, jwtoken: str) -> Optional[Dict[str, Any]]:
        try:
            payload = decodeJWT(jwtoken)
        except Exception:
            payload = None

        return payload
