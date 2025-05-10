from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exc.exception import ValidationError
from app.database.db import get_session
from app.repositories.comment_repository import CommentRepository
from app.repositories.response_repository import CommentResponseRepository
from app.schemas.comment_response_schema import CommentResponseCreate
from app.services.ai_service import AIService, get_ai_service
from app.services.celery_service import CeleryService, get_celery_service


class CommentResponseService:
    def __init__(
        self,
        session: AsyncSession,
        comment_response_repository: CommentResponseRepository,
        comment_repository: CommentRepository,
    ):
        self.session = session
        self.comment_response_repository = comment_response_repository
        self.comment_repository = comment_repository

    async def create_comment_response(
        self,
        comment_response_create: CommentResponseCreate,
        user_id: int,
        comment_id: int,
        auto_response: bool = False,
        ai_service: AIService = Depends(get_ai_service),
        celery_service: CeleryService = Depends(get_celery_service),
        delay: int = 0,
    ):
        data = comment_response_create.model_dump()
        data["user_id"] = user_id
        data["comment_id"] = comment_id

        if auto_response:
            comment = await self.comment_repository.get_one(id=comment_id)
            if comment:
                try:
                    data["content"] = ai_service.create_response_text_to_comment(comment.content)

                    return celery_service.create_comment_response_scheduled(
                        comment_response_create, user_id, comment_id, delay
                    )
                except ValidationError as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"AI service error: {e}",
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment not found",
                )
        try:
            return await self.comment_response_repository.create(data)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment or User not found",
            )

    async def get_comment_responses_for_comment(self, comment_id: int):
        responses = await self.comment_response_repository.get_many(comment_id=comment_id)
        if not responses:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Responses not found")

        return responses


def get_comment_response_service(
    session: AsyncSession = Depends(get_session),
) -> CommentResponseService:
    comment_response_repository = CommentResponseRepository(session)
    comment_repository = CommentRepository(session)

    return CommentResponseService(
        session=session, comment_response_repository=comment_response_repository, comment_repository=comment_repository
    )
