from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import (
    require_admin,
    require_any_user,
    require_author_or_admin,
)
from app.core.database import get_db
from app.user import User

from .schemas import PostCreate, PostPatch, PostResponse, PostUpdate
from .services import PostServices

router = APIRouter(prefix="/post", tags=["Post management"])


@router.post(
    "/create-post/", response_model=PostResponse, status_code=status.HTTP_201_CREATED
)
def create_post(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)],
    post_in: PostCreate,
):
    return PostServices.create(db, post_in)


@router.get("/all/", response_model=list[PostResponse])
def get_all_posts(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_any_user)],
    skip: int = 0,
    limit: int = 10,
):
    return PostServices.get_all(db, skip, limit)


@router.get("/{post_id}/", response_model=PostResponse)
def get_by_id_post(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_any_user)],
    post_id: int,
):
    return PostServices.get_by_id(db, post_id)


@router.delete("delete-post/{post_id}/")
def delete_post(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)],
    post_id: int,
):
    return PostServices.delete(db, post_id)


@router.put("/update-post/{post_id}/")
def update_all_post(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_author_or_admin)],
    post_id: int,
    post_in: PostUpdate,
):
    return PostServices.update_all(db, post_id, post_in)


@router.patch("/update-post/{post_id}/")
def update_item_post(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_author_or_admin)],
    post_id: int,
    post_in: PostPatch,
):
    return PostServices.update_item(db, post_id, post_in)
