from pydantic import BaseModel

from app.enums.posts import PostStatusEnum


class PostBase(BaseModel):
    title: str
    content: str
    status: PostStatusEnum
    comments: list = []


class PostOut(PostBase):
    id: int
    

class PostCreate(PostBase):
    pass
    

class PostUpdate(PostBase):
    pass
