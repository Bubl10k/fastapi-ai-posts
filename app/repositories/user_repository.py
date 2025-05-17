from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base_repository import BaseRepository
from app.utils.s3 import upload_file_to_s3


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def upload_avatar(self, user: User, file: UploadFile):
        avatar_url = upload_file_to_s3(file, user.id)
        user.avatar = avatar_url
        await self.session.commit()
        await self.session.refresh(user)
        return user
