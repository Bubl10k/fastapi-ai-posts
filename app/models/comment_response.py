from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimeStampMixin


class CommentResponse(Base, TimeStampMixin):
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False)
    comment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("comment.id"), nullable=False
    )

    comment = relationship(
        "Comment", back_populates="comment_responses")
    user = relationship(
        "User", back_populates="comment_responses")
