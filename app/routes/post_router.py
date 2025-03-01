from fastapi import APIRouter, Depends, status

from app.schemas.post_schema import PostCreate, PostOutDetail, PostOutList, PostUpdate
from app.services.auth_service import AuthService
from app.dependencies import CurrentUserDependency, PostServiceDependency


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[Depends(AuthService.get_current_user)],
)


@router.get("/", response_model=list[PostOutList])
async def get_all_posts(post_service: PostServiceDependency):
    return await post_service.get_all_posts()


@router.get("/{post_id}", response_model=PostOutDetail)
async def get_post_by_id(post_id: int, post_service: PostServiceDependency):
    return await post_service.get_post_by_id(post_id)


@router.get("/user/{user_id}", response_model=list[PostOutList])
async def get_user_posts(
    post_service: PostServiceDependency, current_user: CurrentUserDependency
):
    return await post_service.get_user_posts(current_user.id)


@router.post("/", response_model=PostOutDetail, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_create: PostCreate,
    current_user: CurrentUserDependency,
    post_service: PostServiceDependency,
):
    return await post_service.create_post(post_create, current_user.id)


@router.put("/{post_id}", response_model=PostOutDetail)
async def update_post_by_id(
    post_id: int, post_update: PostUpdate, post_service: PostServiceDependency
):
    return await post_service.update_post_by_id(post_id, post_update)
