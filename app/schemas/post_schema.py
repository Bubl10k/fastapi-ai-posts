from pydantic import BaseModel

from app.enums.posts import PostStatusEnum
from app.schemas.comment_schema import CommentOut, CommentOutWithUser
from app.schemas.mixins import TimeStampMixin
from app.schemas.post_reaction_schema import PostReactionResponse
from app.schemas.user_schema import UserResponse


class PostBase(BaseModel):
    title: str
    content: str


class PostOut(PostBase):
    id: int
    status: PostStatusEnum = PostStatusEnum.PENDING


class PostWithReactions(PostOut):
    reactions: list[PostReactionResponse] = []


class PostOutDetail(PostWithReactions, TimeStampMixin):
    user: UserResponse


class PostWithComments(PostOutDetail):
    comments: list[CommentOut]


class PostWithUserComments(PostWithComments):
    comments: list[CommentOutWithUser]


class PostOutList(PostWithUserComments, PostWithReactions, TimeStampMixin):
    pass


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass
