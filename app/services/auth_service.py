from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.settings import settings
from app.database.db import get_session
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import LoginResponse, UserCreate, UserLogin, UserMe
from app.services.user_service import UserService, get_user_service

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
token_auth_scheme = HTTPBearer()


class AuthService:
    def __init__(self, session: AsyncSession, user_repository: UserRepository):
        self.session = session
        self.user_repository = user_repository

    async def create_access_token(self, user_id: int, email: str) -> str:
        expiration = datetime.now(timezone.utc) + timedelta(hours=1)
        payload = {
            "id": user_id.__str__(),
            "email": email,
            "exp": expiration,
            "type": "access",
        }
        token = jwt.encode(
            payload, settings.auth.JWT_SECRET_KEY, algorithm=settings.auth.JWT_ALGORITHM
        )
        return token

    async def create_refresh_token(self, user_id: int, email: str) -> str:
        expiration = datetime.now(timezone.utc) + timedelta(days=7)
        payload = {
            "id": user_id.__str__(),
            "email": email,
            "exp": expiration,
            "type": "refresh",
        }
        token = jwt.encode(
            payload, settings.auth.JWT_SECRET_KEY, algorithm=settings.auth.JWT_ALGORITHM
        )
        return token

    async def refresh_token(
        self, refresh_token: str, user_service: UserService
    ) -> LoginResponse:
        try:
            payload = jwt.decode(
                refresh_token,
                settings.auth.JWT_SECRET_KEY,
                algorithms=[settings.auth.JWT_ALGORITHM],
            )
            user_email: str = payload.get("email")
            token_type: str = payload.get("type")

            if user_email is None or token_type != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
                )

            user = await user_service.get_user_by_email(user_email)
            access_token = await self.create_access_token(
                user_id=user.id, email=user.email
            )
            return LoginResponse(access_token=access_token, refresh_token=refresh_token)

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Token has expired",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

    async def login(self, user_login: UserLogin) -> LoginResponse:
        existing_user = await self.user_repository.get_one(email=user_login.email)

        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "There is no user with this email",
                },
            )

        is_valid = self.verify_password(user_login.password, existing_user.password)

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": "Invalid password",
                },
            )

        access_token = await self.create_access_token(
            user_id=existing_user.id, email=existing_user.email
        )
        refresh_token = await self.create_refresh_token(
            user_id=existing_user.id, email=existing_user.email
        )
        return LoginResponse(access_token=access_token, refresh_token=refresh_token)

    async def register(self, user_create: UserCreate) -> LoginResponse:
        existing_user = await self.user_repository.get_one(email=user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "User with this email already exists"},
            )

        hashed_password = self.hash_password(user_create.password)

        new_user = await self.user_repository.create(
            UserCreate(
                email=user_create.email,
                password=hashed_password,
                username=user_create.username,
            ).model_dump()
        )

        access_token = await self.create_access_token(
            user_id=new_user.id, email=new_user.email
        )
        refresh_token = await self.create_refresh_token(
            user_id=new_user.id, email=new_user.email
        )
        return LoginResponse(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(
                token,
                settings.auth.JWT_SECRET_KEY,
                algorithms=[settings.auth.JWT_ALGORITHM],
            )
            user_email: str = payload.get("email")
            token_type: str = payload.get("type")
            if user_email is None or token_type != "access":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
                )
            return user_email
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Token has expired",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

    @staticmethod
    async def get_current_user(
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        user_service: UserService = Depends(get_user_service),
    ) -> UserMe:
        user_email = AuthService.verify_token(token.credentials)
        user = await user_service.get_user_by_email(user_email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        return UserMe(id=user.id, email=user.email)


def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session=session, user_repository=UserRepository(session=session))
