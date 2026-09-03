from datetime import datetime

from pydantic import BaseModel

from app.post.schemas import PostResponse


class CommentBase(BaseModel):
    content: str
    user_id: int
    post_id: int


class CommentResponse(CommentBase):
    id: int
    created_at: datetime

    post: PostResponse

    class Config:
        from_attributes = True
