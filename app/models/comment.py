from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.comments import CommentStatusEnum
from app.models.base import Base, TimeStampMixin


class Comment(Base, TimeStampMixin):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[CommentStatusEnum] = mapped_column(
        Enum(CommentStatusEnum), nullable=False
    )
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("post.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False)

    comment_responses = relationship(
        "CommentResponse", back_populates="comment"
    )
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
