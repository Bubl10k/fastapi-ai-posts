from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession, repository: UserRepository):
        self.session = session
        self.repository = repository

    async def create_user(self, user_create: UserCreate) -> User:
        return await self.repository.create(user_create.model_dump())

    async def get_all_users(self) -> list[User]:
        return await self.repository.get_many()

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.repository.get_one(id=user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user

    async def get_user_by_email(self, email: str) -> User:
        user = await self.repository.get_one(email=email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user

    async def update_user_by_id(self, user_id: int, data: UserUpdate) -> User:
        return await self.repository.update(id=user_id, data=data.model_dump())

    async def delete_user_by_id(self, user_id: int) -> User:
        return await self.repository.delete(id=user_id)


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session, UserRepository(session))
