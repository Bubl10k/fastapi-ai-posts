from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound
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
        auto_response: bool = False,
    ):
        data = comment_response_create.model_dump()
        data["user_id"] = user_id
        data["comment_id"] = comment_id

        if auto_response:
            # TODO: create auto response via AI service
            pass

        try:
            return await self.repository.create(data)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment or User not found",
            )

    async def get_comment_responses_for_comment(self, comment_id: int):
        responses = await self.repository.get_many(comment_id=comment_id)
        if not responses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Responses not found"
            )

        return responses


def get_comment_response_service(
    session: AsyncSession = Depends(get_session),
) -> CommentResponseService:
    return CommentResponseService(
        session=session, repository=CommentResponseRepository(session)
    )
