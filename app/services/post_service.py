from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models.post import Post
from app.repositories.post_repository import PostRepository
from app.schemas.post_schema import PostCreate, PostUpdate


class PostService:
    def __init__(self, session: AsyncSession, repository: PostRepository):
        self.session = session
        self.repository = repository
        
    async def get_all_posts(self):
        return await self.repository.get_many(preload=[Post.user])
    
    async def get_user_posts(self, user_id: int):
        return await self.repository.get_many(preload=[Post.user], user_id=user_id)
    
    async def get_post_by_id(self, post_id: int):
        return await self.repository.get_one(preload=[Post.user], id=post_id)
    
    async def create_post(self, post_create: PostCreate, user_id: int):
        data = post_create.model_dump()
        data['user_id'] = user_id
        return await self.repository.create(data)

    async def update_post_by_id(self, post_id: int, post_update: PostUpdate):
        return await self.repository.update(model_id=post_id, data=post_update.model_dump())

async def get_post_service(session: AsyncSession = Depends(get_session)) -> PostService:
    return PostService(session, PostRepository(session))
