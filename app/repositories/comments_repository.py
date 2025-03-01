from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment
from app.repositories.base_repository import BaseRepository


class CommentsRepository(BaseRepository[Comment]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Comment)
