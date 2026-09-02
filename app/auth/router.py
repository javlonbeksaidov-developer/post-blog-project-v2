from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.user.models import User
from auth.schemas import Token
from auth.services import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Foydalanuvchi username va paroli orqali JWT Access Token beruvchi endpoint.
    """
    # Foydalanuvchini bazadan qidirish
    user = db.query(User).filter(User.username == form_data.username).first()

    # User topilmasa yoki paroli xato bo'lsa
    if not user or not AuthService.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username yoki parol noto'g'ri kiritildi",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Akkaunt aktivligi tekshiriladi
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Foydalanuvchi hisobi faollashtirilmagan",
        )

    # JWT token yaratamiz (payload'ga username beriladi)
    access_token = AuthService.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
