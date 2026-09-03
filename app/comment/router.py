from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from .schemas import CommentBase
from .services import CommentServices

router = APIRouter(prefix="/comment", tags=["Comment management"])


@router.post("/create-comment")
def create_comment(db: Annotated[Session, Depends(get_db)], comment_in: CommentBase):
    return CommentServices.create(db, comment_in)


@router.get("/all")
def get_all_comment(
    db: Annotated[Session, Depends(get_db)], skip: int = 0, limit: int = 0
):
    return CommentServices.get_all(db, skip, limit)


@router.get("/{comment_id}")
def get_by_id_comment(db: Annotated[Session, Depends(get_db)], comment_id: int):
    return CommentServices.get_all(db, comment_id)


@router.delete("/delete/{comment_id}")
def delete_comment(db: Annotated[Session, Depends(get_db)], comment_id: int):
    return CommentServices.delete(db, comment_id)
