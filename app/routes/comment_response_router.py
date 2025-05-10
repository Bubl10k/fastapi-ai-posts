from fastapi import APIRouter, Depends, status

from app.dependencies import (
    AIServiceDependency,
    CeleryServiceDependency,
    CommentResponseServiceDependency,
    CurrentUserDependency,
)
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


@router.post("/", response_model=CommentResponseOutDetail, status_code=status.HTTP_201_CREATED)
async def create_comment_response(
    comment_response_create: CommentResponseCreate,
    comment_id: int,
    user: CurrentUserDependency,
    comment_response_service: CommentResponseServiceDependency,
    ai_service: AIServiceDependency,
    celery_service: CeleryServiceDependency,
    is_auto_response: bool = False,
    delay: int = 0,
):
    return await comment_response_service.create_comment_response(
        comment_response_create=comment_response_create,
        user_id=user.id,
        comment_id=comment_id,
        auto_response=is_auto_response,
        ai_service=ai_service,
        celery_service=celery_service,
        delay=delay,
    )


@router.get("/", response_model=list[CommentResponseOutDetail])
async def get_comment_responses_for_comment(
    comment_id: int,
    comment_response_service: CommentResponseServiceDependency,
):
    return await comment_response_service.get_comment_responses_for_comment(comment_id)
