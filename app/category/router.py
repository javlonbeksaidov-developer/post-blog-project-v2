from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import (
    require_admin,
    require_any_user,
)
from app.core.database import get_db
from app.user import User

from .schemas import CategoryCreate, CategoryResponse, CategoryUpdate
from .services import CategoryServices

router = APIRouter(prefix="/category", tags=["Category management"])


@router.post(
    "/create", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED
)
def create_category(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)],
    category_in: CategoryCreate,
):
    return CategoryServices.create(db, category_in)


@router.get("/all", response_model=list[CategoryResponse])
def get_all_categories(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_any_user)],
    skip: int = 0,
    limit: int = 10,
):
    return CategoryServices.get_all(db, skip, limit)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_by_id_category(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_any_user)],
    category_id: int,
):
    return CategoryServices.get_all(db, category_id)


@router.delete("/delete/{category_id}")
def delete_category(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)],
    category_id: int,
):
    return CategoryServices.delete(db, category_id)


@router.put("/create/{category_id}")
def update_category(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)],
    category_id: int,
    category_in: CategoryUpdate,
):
    return CategoryServices.update(db, category_id, category_in)
