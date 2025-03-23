from pydantic import BaseModel

from app.enums.posts import PostStatusEnum
from app.schemas.comment_schema import CommentOut
from app.schemas.mixins import TimeStampMixin
from app.schemas.user_schema import UserOut


class PostBase(BaseModel):
    title: str
    content: str


class PostOut(PostBase):
    id: int
    status: PostStatusEnum = PostStatusEnum.PENDING


class PostOutDetail(PostOut, TimeStampMixin):
    user: UserOut


class PostOutList(PostOut):
    pass


class PostWithComments(PostOutDetail):
    comments: list[CommentOut]


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass
