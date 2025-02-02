from fastapi import APIRouter

from app.shemas.user_schema import UserCreate, UserOut, UserUpdate
from app.utils.dependencies import UserServiceDependency

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut)
async def create_user(user_create: UserCreate, user_service: UserServiceDependency):
    return await user_service.create_user(user_create)


@router.get("/", response_model=list[UserOut])
async def get_all_users(user_service: UserServiceDependency):
    return await user_service.get_all_users()


@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: int, user_service: UserServiceDependency):
    return await user_service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserOut)
async def update_user_by_id(
    user_id: int, user_update: UserUpdate, user_service: UserServiceDependency
):
    return await user_service.update_user_by_id(user_id, user_update)


@router.delete("/{user_id}", response_model=UserOut)
async def delete_user_by_id(user_id: int, user_service: UserServiceDependency):
    return await user_service.delete_user_by_id(user_id)
