from datetime import datetime

from pydantic import BaseModel


class LikeBase(BaseModel):
    user_id: int
    post_id: int


class LikeResponse(LikeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
