from pydantic import BaseModel

from app.enums.posts import PostStatusEnum
from app.schemas.comment_schema import CommentOut
from app.schemas.mixins import TimeStampMixin
from app.schemas.post_reaction_schema import PostReactionResponse
from app.schemas.user_schema import UserOut


class PostBase(BaseModel):
    title: str
    content: str


class PostOut(PostBase):
    id: int
    status: PostStatusEnum = PostStatusEnum.PENDING


class PostWithReactions(PostOut):
    reactions: list[PostReactionResponse]


class PostOutDetail(PostWithReactions, TimeStampMixin):
    user: UserOut


class PostOutList(PostWithReactions):
    pass


class PostWithComments(PostOutDetail):
    comments: list[CommentOut]


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass
