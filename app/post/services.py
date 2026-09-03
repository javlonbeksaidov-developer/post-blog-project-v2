from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Post
from .schemas import PostCreate, PostPanch, PostUpdate


class PostServices:
    @staticmethod
    def get_all_posts(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Post).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id_post(db: Session, post_id: int) -> Post:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!"
            )
        return post

    @staticmethod
    def create_post(db: Session, post_in: PostCreate) -> Post:
        new_post = Post(**post_in.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

    @staticmethod
    def update_all(db: Session, post_id: int, post_in: PostUpdate) -> Post:
        post = PostServices.get_by_id_post(db, post_id)

        post.title = post_in.title
        post.content = post_in.content
        post.image = post_in.image
        post.author_id = post_in.author_id
        post.category_id = post.category_id

        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def update_item(db: Session, post_id: int, post_in: PostPanch) -> Post:
        post = PostServices.get_by_id_post(db, post_id)

        update_post = post_in.model_dump(exclude_unset=True)
        for key, value in update_post.items():
            setattr(post, key, value)

        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def delete_post(db: Session, post_id: int):
        post = PostServices.get_by_id_post(db, post_id)
        db.delete(post)
        db.commit()
        return {"messaage": "deleted post!"}
