from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.core.database import Base


class UserRoles(str, Enum):
    ADMIN = "admin"
    AUTHOR = "author"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRoles), default=UserRoles.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    like = relationship("Like", back_populates="user")
    comment = relationship("Comment", back_populates="user")
    post = relationship("Post", back_populates="user") # author_id
