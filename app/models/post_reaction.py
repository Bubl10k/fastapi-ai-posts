from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.posts import PostReactionEnum
from app.models import Base
from app.models.base import TimeStampMixin, UUIDMixin


class PostReaction(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "post_reactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    reaction: Mapped[PostReactionEnum] = mapped_column(Enum(PostReactionEnum), nullable=False)

    user = relationship("User")
    post = relationship("Post", back_populates="reactions")
