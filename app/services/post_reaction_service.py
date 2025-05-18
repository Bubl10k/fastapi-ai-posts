from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_session
from app.repositories.post_reaction_repository import PostReactionRepository
from app.schemas.post_reaction_schema import PostReactionCreate


class PostReactionService:
    def __init__(self, session: AsyncSession, repository: PostReactionRepository):
        self.session = session
        self.repository = repository

    async def create_reaction(self, post_id: int, user_id: int, post_reaction_create: PostReactionCreate):
        data = post_reaction_create.model_dump()
        data["post_id"] = post_id
        data["user_id"] = user_id

        try:
            return await self.repository.create(data)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or Reaction already exists"
            )

    async def update_reaction_by_id(self, reaction_id: int, reaction_update: PostReactionCreate):
        reaction = await self.repository.update(model_id=reaction_id, data=reaction_update.model_dump())

        if not reaction:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reaction not found")

        return reaction


def get_post_reaction_service(session: AsyncSession = Depends(get_session)) -> PostReactionService:
    return PostReactionService(session, PostReactionRepository(session))
