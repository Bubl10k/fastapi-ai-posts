from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.repositories.base_repository import BaseRepository


class PostRepository(BaseRepository[Post]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Post)

    async def get_post_with_responses(self, preload: list | None = None, **params) -> Post:
        query = select(self.model).filter_by(**params)

        if preload:
            for option in preload:
                query = query.options(option)

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_posts_with_comments(
        self,
        user_id: int,
        preload: list | None = None,
    ) -> list[Post]:
        query = select(self.model).where(Post.user_id == user_id)

        if preload:
            for option in preload:
                query = query.options(option)

        result = await self.session.execute(query)
        return result.scalars().all()
