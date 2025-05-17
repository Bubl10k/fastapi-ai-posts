from fastapi import APIRouter, Depends, UploadFile

from app.dependencies import CurrentUserDependency, UserServiceDependency
from app.schemas.user_schema import UserResponse, UserUpdate
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(AuthService.get_current_user)],
)


@router.get("/", response_model=list[UserResponse])
async def get_all_users(user_service: UserServiceDependency):
    return await user_service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, user_service: UserServiceDependency):
    return await user_service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user_by_id(user_id: int, user_update: UserUpdate, user_service: UserServiceDependency):
    return await user_service.update_user_by_id(user_id, user_update)


@router.post("/{user_id}", response_model=UserResponse)
async def upload_user_avatar(user: CurrentUserDependency, file: UploadFile, user_service: UserServiceDependency):
    return await user_service.upload_user_avatar(user.id, file)
