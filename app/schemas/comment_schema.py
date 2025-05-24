from pydantic import BaseModel

from app.enums.comments import CommentStatusEnum
from app.schemas.comment_response_schema import CommentResponseOutDetail
from app.schemas.mixins import TimeStampMixin
from app.schemas.user_schema import UserResponse


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentOut(CommentBase, TimeStampMixin):
    id: int
    status: CommentStatusEnum
    post_id: int
    comment_responses: list[CommentResponseOutDetail]


class CommentOutWithUser(CommentOut):
    user: UserResponse


class CommentUpdate(CommentBase):
    pass
