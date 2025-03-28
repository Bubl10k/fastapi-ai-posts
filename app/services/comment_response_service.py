from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_session
from app.repositories.response_repository import CommentResponseRepository
from app.schemas.comment_response_schema import CommentResponseCreate


class CommentResponseService:
    def __init__(self, session: AsyncSession, repository: CommentResponseRepository):
        self.session = session
        self.repository = repository

    async def create_comment_response(
        self,
        comment_response_create: CommentResponseCreate,
        user_id: int,
        comment_id: int,
    ):
        data = comment_response_create.model_dump()
        data["user_id"] = user_id
        data["comment_id"] = comment_id

        try:
            return await self.repository.create(data)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment or User not found",
            )


def get_comment_response_service(
    session: AsyncSession = Depends(get_session),
) -> CommentResponseService:
    return CommentResponseService(
        session=session, repository=CommentResponseRepository(session)
    )
