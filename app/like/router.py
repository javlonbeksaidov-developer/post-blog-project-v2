from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_any_user
from app.core.database import get_db
from app.user import User

from .schemas import LikeBase
from .services import LikeServices

router = APIRouter(tags=["Like management"])


@router.post("/like")
def like_post(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_any_user)],
    like_in: LikeBase,
):
    return LikeServices.like(db, like_in)


@router.delete("/dislike/{like_id}")
def dislike_post(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_any_user)],
    like_id: int,
):
    return LikeServices.like(db, like_id)
