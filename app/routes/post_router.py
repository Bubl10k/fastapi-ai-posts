from fastapi import APIRouter


from app.schemas.post_schema import PostCreate, PostOut
from app.utils.dependencies import CurrentUserDependency, PostServiceDependency


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[PostOut])
async def get_all_posts(post_service: PostServiceDependency):
    return await post_service.get_all_posts()


@router.get("/{post_id}", response_model=PostOut)
async def get_post_by_id(post_id: int, post_service: PostServiceDependency):
    return await post_service.get_post_by_id(post_id)


@router.get("/user/{user_id}", response_model=list[PostOut])
async def get_user_posts(
    post_service: PostServiceDependency, current_user: CurrentUserDependency
):
    return await post_service.get_user_posts(current_user)


@router.post("/", response_model=PostOut)
async def create_post(post_create: PostCreate, post_service: PostServiceDependency):
    return await post_service.create_post(post_create, post_create.user_id)
