from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Category
from .schemas import CategoryCreate, CategoryUpdate


class CategoryServices:
    @staticmethod
    def create(db: Session, category_in: CategoryCreate) -> Category:
        new_category = Category(**category_in.model_dump())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Category).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, category_id: int):
        category = db.query(Category).filter(Category.id == category_id).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )

        return category

    @staticmethod
    def delete(db: Session, category_id: int):
        category = CategoryServices.get_by_id(db, category_id)
        db.delete(category)
        db.commit()
        return {"message": "Category deleted!"}

    @staticmethod
    def update(db: Session, category_id: int, category_in: CategoryUpdate):
        category = CategoryServices.get_by_id(db, category_id)

        category.name = category_in.name
        category.description = category_in.description

        db.commit()
        db.refresh(category)
        return category
