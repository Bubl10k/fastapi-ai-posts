from app.enums.base import BaseEnum


class PostStatusEnum(BaseEnum):
    VALID = "valid"
    PENDING = "pending"
    BLOCKED = "blocked"
