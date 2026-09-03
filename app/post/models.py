from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.core.database import Base


class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    image = Column(String(255))
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    status = Column(SQLEnum(PostStatus), default=PostStatus.DRAFT, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=None)

    like = relationship("Like", back_populates="post")
    comment = relationship("Comment", back_populates="post")
    user = relationship("User", back_populates="post")
    category = relationship("Category", back_populates="post")