from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from .models import Post
from .schemas import PostCreate, PostUpdate

router = APIRouter(prefix="/post", tags=["Post management"])

@router.post("/create-post/")
def create_post():
    pass