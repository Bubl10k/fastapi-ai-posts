from fastapi import APIRouter
from fastapi.params import Depends

from app.dependencies import CurrentUserDependency, PostReactionDependency
from app.schemas.post_reaction_schema import PostReactionCreate, PostReactionResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/posts/{post_id}/reactions", tags=["Post reactions"], dependencies=[Depends(AuthService.get_current_user)]
)


@router.post("/", status_code=201, response_model=PostReactionResponse)
async def create_post_reaction(
    post_reaction_create: PostReactionCreate,
    post_id: int,
    user: CurrentUserDependency,
    post_reaction_service: PostReactionDependency,
):
    return await post_reaction_service.create_reaction(post_id, user.id, post_reaction_create)


@router.put("/{reaction_id}", response_model=PostReactionResponse)
async def update_post_reaction(
    reaction_id: int,
    reaction_update: PostReactionCreate,
    post_reaction_service: PostReactionDependency,
):
    return await post_reaction_service.update_reaction_by_id(reaction_id, reaction_update)
