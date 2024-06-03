from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.dao.auth_dao import AuthDAO
from app.schema import MediaSchema, Login
from app.router.base_router import BaseCRUDRouter

class AuthRouter(BaseCRUDRouter):

    def __init__(self, dao: AuthDAO = AuthDAO(User), prefix: str = "", tags: List[str] = []):
        super().__init__(dao=dao, schemas=MediaSchema, prefix=prefix,tags = tags, show_default_routes=False)
        self.dao = dao
        self.register_routes()

    def register_routes(self):
        @self.router.post("/")
        async def user_login(request: Login, db: AsyncSession = Depends(self.get_db)):
           
            current_user : User = await self.dao.user_exists(db_session=db, email=request.username)

            if current_user is None:
                raise HTTPException(status_code=401, detail="User not found")
        
            if current_user.is_verified and (current_user.login_provider == "native" or current_user.login_provider is None):
                if current_user.password is None:
                    raise HTTPException(status_code=401, detail="Please set your password first!")
                
                if await self.dao.verify_password(db_session=db, login_info=request):
                    current_user.update_last_login_time()

                    return await self.dao.authenticate_user(current_user=current_user)
                else:
                    raise HTTPException(status_code=401, detail="Wrong login details!")
            else:
                raise HTTPException(status_code=401, detail="User account not verified or using a login provider")
            
        @self.router.get("/verify-email")
        async def verify_email(email: str, token: str, db: AsyncSession = Depends(self.get_db)):
            current_user : User = await self.dao.user_exists(db_session=db, email=email)

            if current_user is None:
                raise HTTPException(status_code=400, detail="User not found")
            
            if not current_user.is_verified and current_user.verification_token == token:
                current_user.is_verified = True
                current_user.verification_token = None
                response = await self.dao.commit_and_refresh(db_session=db, obj=current_user)

                if response:
                    return {"data": "User successfully verified!"}
                else:
                    raise HTTPException(status_code=400, detail="User account not verified or using a login provider")
            else:
                raise HTTPException(status_code=400, detail="User account not verified or using a login provider")
        
        @self.router.get("/mail-unsubscribe")
        async def mail_unsubscribe(email: str, token: str, db: AsyncSession = Depends(self.get_db)):
           
            current_user : User = await self.dao.user_exists(db_session=db, email=email)

            if current_user is None:
                raise HTTPException(status_code=400, detail="User not found")
            
            if current_user.is_subscribed and current_user.is_subscribed_token == token:
                current_user.is_subscribed = False
                current_user.is_subscribed_token = None
                response = await self.dao.commit_and_refresh(db_session=db, obj=current_user)

                if response:
                    return {"data": "User successfully unsubsribed!"}
                else:
                    raise HTTPException(status_code=400, detail="User account not verified or using a login provider")
            else:
                raise HTTPException(status_code=400, detail="User account not verified or using a login provider")