from fastapi import APIRouter

from app.dependencies import AuthServiceDependency, UserServiceDependency
from app.schemas.user_schema import LoginResponse, UserCreate, UserLogin, UserMe

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
async def login_by_email_and_password(
    user_data: UserLogin, auth_service: AuthServiceDependency
):
    return await auth_service.login(user_data)


@router.post("/register", response_model=LoginResponse)
async def register_user(user_data: UserCreate, auth_service: AuthServiceDependency):
    return await auth_service.register(user_data)


@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(
    refresh_token: str,
    auth_service: AuthServiceDependency,
    user_service: UserServiceDependency
):
    return await auth_service.refresh_token(refresh_token, user_service)


@router.post("/me", response_model=UserMe)
async def get_current_user(
    auth_service: AuthServiceDependency,
) -> UserMe:
    return await auth_service.get_current_user()
