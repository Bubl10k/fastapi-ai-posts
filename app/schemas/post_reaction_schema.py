from pydantic import BaseModel

from app.enums.posts import PostReactionEnum


class PostReactionBase(BaseModel):
    reaction: PostReactionEnum


class PostReactionCreate(PostReactionBase):
    pass


class PostReactionResponse(PostReactionBase):
    id: int
    user_id: int
    post_id: int
