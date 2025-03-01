from pydantic import BaseModel

from app.enums.posts import PostStatusEnum
from app.schemas.mixins import TimeStampMixin


class PostBase(BaseModel):
    title: str
    content: str


class PostOut(PostBase, TimeStampMixin):
    id: int
    status: PostStatusEnum = PostStatusEnum.PENDING


class PostWithComments(PostBase):
    comments: list = []


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass
