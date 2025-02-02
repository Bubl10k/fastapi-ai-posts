from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, Integer, ForeignKey

from app.enums.comments import CommentStatusEnum
from app.models.base import Base, TimeStampMixin


class Comment(Base, TimeStampMixin):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[CommentStatusEnum] = mapped_column(
        Enum(CommentStatusEnum), nullable=False
    )
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    user: Mapped["User"] = relationship("User", back_populates="comments")
