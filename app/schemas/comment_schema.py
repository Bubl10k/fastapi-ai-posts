from pydantic import BaseModel

from app.enums.comments import CommentStatusEnum
from app.schemas.mixins import TimeStampMixin, UserMixin


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentOut(CommentBase, TimeStampMixin, UserMixin):
    id: int
    status: CommentStatusEnum
    post_id: int


class CommentUpdate(CommentBase):
    pass
