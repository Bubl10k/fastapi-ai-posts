from uuid import UUID

from pydantic import BaseModel

from app.enums.posts import PostReactionEnum


class PostReactionBase(BaseModel):
    reaction: PostReactionEnum


class PostReactionCreate(PostReactionBase):
    pass


class PostReactionResponse(PostReactionBase):
    uuid: UUID
    user_id: int
    post_id: int
