from pydantic import BaseModel

from app.schemas.mixins import TimeStampMixin


class CommentResponseBase(BaseModel):
    content: str


class CommentResponseCreate(CommentResponseBase):
    pass


class CommentResponseOutDetail(CommentResponseBase, TimeStampMixin):
    id: int
    user_id: int
    comment_id: int
