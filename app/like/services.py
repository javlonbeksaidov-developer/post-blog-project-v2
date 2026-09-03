from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.post.services import PostServices
from app.user.services import UserService

from .models import Like
from .schemas import LikeBase


class LikeServices:
    @staticmethod
    def like(db: Session, like_in: LikeBase):
        like = Like(**like_in.model_dump())

        UserService.get_by_id(db, like_in.user_id)
        PostServices.get_by_id(db, like_in.post_id)

        db.add(like)
        db.commit()
        db.refresh(like)
        return like

    @staticmethod
    def dislike(db: Session, like_id):
        like = db.query(Like).filter(Like.id == like_id).first()
        if not like:
            raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Dislike")

        db.delete(like)
        db.commit()
        return {"message": "dislike"}
