from fastapi import APIRouter, Depends, status

from app.dependencies import (
    AIServiceDependency,
    CurrentUserDependency,
    PostServiceDependency,
)
from app.schemas.post_schema import (
    PostCreate,
    PostOut,
    PostOutDetail,
    PostOutList,
    PostUpdate,
    PostWithComments,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[Depends(AuthService.get_current_user)],
)

search_fields = ["title", "content"]


@router.get("/", response_model=list[PostOutList])
async def get_all_posts(post_service: PostServiceDependency):
    return await post_service.get_all_posts()


@router.get("/search", response_model=list[PostOutList])
async def search_posts(
    search_query: str,
    post_service: PostServiceDependency,
):
    return await post_service.search_posts(query=search_query, search_fields=search_fields)


@router.get("/{post_id}", response_model=PostWithComments)
async def get_post_by_id(post_id: int, post_service: PostServiceDependency):
    return await post_service.get_post_by_id(post_id)


@router.get("/user/{user_id}", response_model=list[PostWithComments])
async def get_user_posts(post_service: PostServiceDependency, current_user: CurrentUserDependency):
    return await post_service.get_user_posts(current_user.id)


@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_create: PostCreate,
    current_user: CurrentUserDependency,
    post_service: PostServiceDependency,
    ai_service: AIServiceDependency,
):
    return await post_service.create_post(post_create, current_user.id, ai_service)


@router.put("/{post_id}", response_model=PostOutDetail)
async def update_post_by_id(post_id: int, post_update: PostUpdate, post_service: PostServiceDependency):
    return await post_service.update_post_by_id(post_id, post_update)
