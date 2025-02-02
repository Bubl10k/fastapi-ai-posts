from app.enums.base import BaseEnum


class CommentStatusEnum(BaseEnum):
    VALID = "valid"
    PENDING = "pending"
    INVALID = "invalid"
    