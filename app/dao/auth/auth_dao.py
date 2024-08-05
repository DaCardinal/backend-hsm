from fastapi import Request
from sqlalchemy.orm.exc import NoResultFound
from fastapi_sso.sso.google import GoogleSSO
from sqlalchemy.ext.asyncio import AsyncSession

# models
from app.models.user import User

# daos
from app.dao.auth.user_dao import UserDAO
from app.dao.resources.base_dao import BaseDAO

# utils
from app.utils.hashing import Hash
from app.utils.settings import settings
from app.utils.response import DAOResponse
from app.utils.jwt.auth_handler import signJWT

# schemas
from app.schema.auth import Login, TokenExposed

CLIENT_ID = settings.GOOGLE_SIGNIN_CLIENT_ID
CLIENT_SECRET = settings.GOOGLE_SIGNIN_CLIENT_SECRET

google_sso = GoogleSSO(CLIENT_ID, CLIENT_SECRET, settings.GOOGLE_CALLBACK)


class AuthDAO(BaseDAO[User]):
    def __init__(self):
        self.model = User
        self.user_dao = UserDAO()

        super().__init__(self.model)

    # TODO: Implement google auth
    async def google_login(self):
        with google_sso:
            return await google_sso.get_login_redirect()

    async def google_callback(self, db_session: AsyncSession, request: Request):
        with google_sso:
            try:
                user = await google_sso.verify_and_process(request)

                existing_user: User = await self.query(
                    db_session=db_session, filters={"email": user.username}, single=True
                )

                if existing_user:
                    if not existing_user.is_verified:
                        return DAOResponse[str](
                            success=True, data="User account not verified"
                        )

                    if existing_user.login_provider is not None:
                        existing_user.update_last_login_time()

                        return signJWT(existing_user)
                    else:
                        pass

                else:
                    # create a new user and set login provider for new user
                    await self.user_dao.create(
                        db_session=db_session,
                        obj_in={
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email,
                            "phone_number": "String",
                            "password_hash": "String",
                            "date_of_birth": "String",
                            "is_verified": False,
                            "login_provider": user.provider,
                            "gender": "male",
                        },
                    )

                    created_user: User = await self.query(
                        db_session=db_session,
                        filters={"email": user.username},
                        single=True,
                    )
                    created_user.update_last_login_time()

                    return signJWT(created_user)

            except Exception as e:
                return DAOResponse[str](
                    success=True, data=f"Google Sign-In failed: {str(e)}"
                )

    async def verify_password(self, db_session: AsyncSession, login_info: Login):
        current_user: User = await self.query(
            db_session=db_session, filters={"email": login_info.username}, single=True
        )

        if current_user is None:
            raise NoResultFound()

        return Hash.verify(current_user.password, login_info.password)

    async def authenticate_user(self, current_user: User) -> DAOResponse[TokenExposed]:
        return signJWT(current_user)

    async def user_exists(self, db_session: AsyncSession, email: str):
        current_user: User = await self.query(
            db_session=db_session, filters={"email": email}, single=True
        )

        return current_user

    # TODO: Remove attempt login
    async def attempt_login(
        self, db_session: AsyncSession, request: dict
    ) -> DAOResponse[TokenExposed | str]:
        current_user: User = self.user_exists(
            db_session=db_session, email=request.email
        )

        if current_user is None:
            raise NoResultFound()

        if current_user.is_verified and (
            current_user.login_provider == "native"
            or current_user.login_provider is None
        ):
            if current_user.password is None:
                return DAOResponse[str](
                    success=False, data="Please set your password first!"
                )

            if self.verify_password(db_session=db_session, login_info=request):
                current_user.update_last_login_time()

                return self.authenticate_user(current_user.to_dict())
            else:
                return DAOResponse[str](success=False, data="Wrong login details!")
        else:
            return DAOResponse[str](
                success=False,
                data="User account not verified or using a login provider",
            )
