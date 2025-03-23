from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment_response import CommentResponse
from app.repositories.base_repository import BaseRepository


class CommentResponseRepository(BaseRepository[CommentResponse]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, CommentResponse)
