from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_session
from app.enums.posts import PostStatusEnum
from app.models.post import Post
from app.repositories.post_repository import PostRepository
from app.schemas.post_schema import PostCreate, PostUpdate
from app.services.ai_service import AIService, get_ai_service


class PostService:
    def __init__(self, session: AsyncSession, repository: PostRepository):
        self.session = session
        self.repository = repository

    async def get_all_posts(self):
        return await self.repository.get_many(preload=[Post.user])

    async def get_user_posts(self, user_id: int):
        return await self.repository.get_many(preload=[Post.user], user_id=user_id)

    async def get_post_by_id(self, post_id: int):
        post = await self.repository.get_one(
            preload=[Post.user, Post.comments], id=post_id
        )
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

        return post

    async def create_post(
        self,
        post_create: PostCreate,
        user_id: int,
        ai_service: AIService = Depends(get_ai_service)
    ):
        data = post_create.model_dump()
        is_safe = ai_service.is_content_appropriate(data["content"])
        
        if not is_safe:
            data["status"] = PostStatusEnum.BLOCKED
            data["user_id"] = user_id
            return await self.repository.create(data)
        
        data["status"] = PostStatusEnum.PENDING
        data["user_id"] = user_id
        
        return await self.repository.create(data)

    async def update_post_by_id(self, post_id: int, post_update: PostUpdate):
        try:
            return await self.repository.update(
                model_id=post_id, data=post_update.model_dump()
            )
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )


async def get_post_service(session: AsyncSession = Depends(get_session)) -> PostService:
    return PostService(session, PostRepository(session))
