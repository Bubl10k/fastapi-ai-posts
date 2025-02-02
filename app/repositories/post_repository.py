from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.repositories.base_repository import BaseRepository


class PostRepository(BaseRepository[Post]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Post)
        