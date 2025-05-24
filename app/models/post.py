from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.posts import PostStatusEnum
from app.models.base import Base, TimeStampMixin


class Post(Base, TimeStampMixin):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[PostStatusEnum] = mapped_column(Enum(PostStatusEnum), nullable=False)
    auto_response: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)

    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan", lazy="selectin")
    user = relationship("User", back_populates="posts", lazy="selectin")
    reactions = relationship("PostReaction", back_populates="post", cascade="all, delete-orphan")
    # tags = relationship("Tag", secondary=post_tags, back_populates="posts", lazy="selectin")
