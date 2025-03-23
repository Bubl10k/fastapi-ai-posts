from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_session
from app.enums.comments import CommentStatusEnum
from app.models.comment import Comment
from app.repositories.comments_repository import CommentsRepository
from app.schemas.comment_schema import CommentCreate, CommentUpdate
from app.services.ai_service import AIService, get_ai_service


class CommentService:
    def __init__(self, session: AsyncSession, repository: CommentsRepository):
        self.session = session
        self.repository = repository

    async def get_post_comments(self, post_id: int):
        posts = await self.repository.get_many(
            post_id=post_id, preload=[Comment.user, Comment.post]
        )

        if not posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

        return posts

    async def create_comment(
        self,
        comment_create: CommentCreate,
        user_id: int,
        post_id: int,
        ai_service: AIService = Depends(get_ai_service),
    ):
        data = comment_create.model_dump()
        response = ai_service.is_content_appropriate(data["content"])

        try:
            comment_status = CommentStatusEnum(response)
        except ValueError:
            comment_status = CommentStatusEnum.PENDING

        data["user_id"] = user_id
        data["post_id"] = post_id
        data["status"] = comment_status

        try:
            comment = await self.repository.create(data)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post or User not found"
            )

        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post or User not found"
            )

        return comment

    async def update_comment_by_id(
        self, comment_id: int, comment_update: CommentUpdate
    ):
        comment = await self.repository.update(
            model_id=comment_id, data=comment_update.model_dump()
        )

        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
            )

        return comment


def get_comment_service(session: AsyncSession = Depends(get_session)) -> CommentService:
    return CommentService(session=session, repository=CommentsRepository(session))
