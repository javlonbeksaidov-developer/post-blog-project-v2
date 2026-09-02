from typing import Annotated

from auth.dependencies import get_current_user, require_admin
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.user.models import User
from app.user.schemas import UserCreate, UserPatch, UserResponse, UserUpdate
from app.user.services import UserService

router = APIRouter(prefix="/users", tags=["Users"])


# 1. READ ALL (GET) - Barcha foydalanuvchilarni olish (Faqat Admin)
@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)],  # Ruxsat tekshiruvi
    skip: int = 0,
    limit: int = 100,
):
    return UserService.get_all(db, skip, limit)


# 2. READ ME (GET) - Joriy login qilgan user o'z profilini ko'rishi
@router.get("/me", response_model=UserResponse)
def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


# 3. READ ONE (GET) - ID bo'yicha foydalanuvchini olish
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
):
    return UserService.get_by_id(db, user_id)


# 4. CREATE (POST) - Yangi foydalanuvchi yaratish (Register)
@router.post(
    "/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(
    user_in: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    return UserService.create(db, user_in)


# 5. FULL UPDATE (PUT) - Foydalanuvchini to'liq yangilash (Faqat Admin)
@router.put("/{user_id}", response_model=UserResponse)
def update_user_full(
    user_id: int,
    user_in: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)],
):
    return UserService.update_full(db, user_id, user_in)


# 6. PARTIAL UPDATE (PATCH) - Foydalanuvchini qisman yangilash
@router.patch("/{user_id}", response_model=UserResponse)
def update_user_partial(
    user_id: int,
    user_in: UserPatch,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    # User faqat o'zini tahrirlashi mumkin, agar Admin bo'lmasa
    if current_user.id != user_id and current_user.role != "admin":
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Siz faqat o'zingizning profilingizni tahrirlay olasiz",
        )

    return UserService.update_partial(db, user_id, user_in)


# 7. DELETE (DELETE) - Foydalanuvchini o'chirish (Faqat Admin)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)],
):
    UserService.delete(db, user_id)
    return False