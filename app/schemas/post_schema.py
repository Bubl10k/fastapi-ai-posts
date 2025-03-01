from pydantic import BaseModel

from app.enums.posts import PostStatusEnum
from app.schemas.mixins import TimeStampMixin, UserMixin


class PostBase(BaseModel):
    title: str
    content: str


class PostOut(PostBase):
    id: int
    status: PostStatusEnum = PostStatusEnum.PENDING


class PostOutDetail(PostOut, TimeStampMixin, UserMixin):
    pass


class PostOutList(PostOut):
    pass


class PostWithComments(PostOutDetail):
    comments: list = []


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass
