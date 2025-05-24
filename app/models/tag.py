from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("post.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.uuid"), primary_key=True),
)


class Tag(Base, UUIDMixin):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # posts = relationship("Post", secondary=post_tags, back_populates="tags")
