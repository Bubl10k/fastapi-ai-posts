from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post_reaction import PostReaction
from app.repositories.base_repository import BaseRepository


class PostReactionRepository(BaseRepository[PostReaction]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, PostReaction)
