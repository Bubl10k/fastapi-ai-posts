from fastapi import APIRouter

from app.schemas.user_schema import LoginResponse, UserCreate, UserLogin
from app.dependencies import AuthServiceDependency


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
async def login_by_email_and_password(
    user_data: UserLogin, auth_service: AuthServiceDependency
):
    return await auth_service.login(user_data)


@router.post("/register", response_model=LoginResponse)
async def register_user(user_data: UserCreate, auth_service: AuthServiceDependency):
    return await auth_service.register(user_data)
