from fastapi import Depends, HTTPException, UploadFile, status
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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    async def get_user_by_email(self, email: str) -> User:
        user = await self.repository.get_one(email=email)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    async def update_user_by_id(self, user_id: int, data: UserUpdate) -> User:
        return await self.repository.update(model_id=user_id, data=data.model_dump())

    async def delete_user_by_id(self, user_id: int) -> User:
        return await self.repository.delete(model_id=user_id)

    async def upload_user_avatar(self, user_id: int, file: UploadFile) -> User:
        user = await self.get_user_by_id(user_id)

        return await self.repository.upload_avatar(user, file)

    async def follow_user(self, user_id: int, friend_id: int) -> User:
        user = await self.get_user_by_id(user_id)
        friend = await self.get_user_by_id(friend_id)

        if friend in user.friends:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are already following this user")

        user.friends.append(friend)
        await self.session.commit()
        await self.session.refresh(user)
        return user


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session, UserRepository(session))
