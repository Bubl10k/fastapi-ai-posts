from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.repositories.post_repository import PostRepository


class PostService:
    def __init__(self, session: AsyncSession, repository: PostRepository):
        self.session = session
        self.repository = repository


async def get_post_service(session: AsyncSession = Depends(get_session)) -> PostService:
    return PostService(session, PostRepository(session))
