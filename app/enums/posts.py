from app.enums.base import BaseEnum


class PostStatusEnum(BaseEnum):
    VALID = "valid"
    PENDING = "pending"
    BLOCKED = "blocked"


class PostReactionEnum(BaseEnum):
    LIKE = "like"
    DISLIKE = "dislike"
