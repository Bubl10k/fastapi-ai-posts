from pydantic import BaseModel

from app.models.base import TimeStampMixin


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentOut(CommentBase, TimeStampMixin):
    pass


class CommentUpdate(CommentBase):
    pass
