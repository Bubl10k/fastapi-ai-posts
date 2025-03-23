from fastapi import APIRouter, Depends, status

from app.dependencies import CommentResponseServiceDependency, CurrentUserDependency
from app.schemas.comment_response_schema import (
    CommentResponseCreate,
    CommentResponseOutDetail,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/comments/{comment_id}/responses",
    tags=["Comment responses"],
    dependencies=[Depends(AuthService.get_current_user)],
)


@router.post(
    "/", response_model=CommentResponseOutDetail, status_code=status.HTTP_201_CREATED
)
async def create_comment_response(
    comment_response_create: CommentResponseCreate,
    comment_id: int,
    user: CurrentUserDependency,
    comment_response_service: CommentResponseServiceDependency,
):
    return await comment_response_service.create_comment_response(
        comment_response_create, user.id, comment_id
    )
