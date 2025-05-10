from fastapi import APIRouter, Depends, Response, status

from app.dependencies import (
    AIServiceDependency,
    CommentServiceDependency,
    CurrentUserDependency,
)
from app.schemas.comment_schema import CommentCreate, CommentOut
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
    dependencies=[Depends(AuthService.get_current_user)],
)


@router.get("/", response_model=list[CommentOut])
async def get_post_comments(post_id: int, comment_service: CommentServiceDependency):
    return await comment_service.get_post_comments(post_id)


@router.post("/", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_create: CommentCreate,
    post_id: int,
    user: CurrentUserDependency,
    comment_service: CommentServiceDependency,
    ai_service: AIServiceDependency,
):
    return await comment_service.create_comment(comment_create, user.id, post_id, ai_service)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, comment_service: CommentServiceDependency):
    await comment_service.delete_comment_by_id(comment_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
