from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Comment
from .schemas import CommentBase


class CommentServices:
    @staticmethod
    def create(db: Session, comment_in: CommentBase):
        comment = Comment(**comment_in.model_dump())
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 0):
        return db.query(Comment).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, comment_id: int):
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
            )
        return comment

    @staticmethod
    def delete(db: Session, comment_id: int):
        comment = CommentServices.get_by_id(db, comment_id)
        db.delete(comment)
        db.commit()
        return {"message": "comment deleted"}
