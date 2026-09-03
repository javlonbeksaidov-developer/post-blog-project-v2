from datetime import datetime

from pydantic import BaseModel

from app.category.schemas import CategoryResponse
from app.user.schemas import UserResponse

from .models import PostStatus


class PostCreate(BaseModel):
    title: str
    content: str
    image: str
    author_id: int
    category_id: int


class PostUpdate(BaseModel):
    title: str
    content: str
    image: str
    author_id: int
    category_id: int


class PostPatch(BaseModel):
    title: str | None = None
    content: str | None = None
    image: str | None = None
    author_id: int | None = None
    category_id: int | None = None


class PostResponse(PostCreate):
    id: int
    status: PostStatus
    created_at: datetime
    updated_at: datetime

    user: UserResponse
    category: CategoryResponse

    class Config:
        from_attributes = True
