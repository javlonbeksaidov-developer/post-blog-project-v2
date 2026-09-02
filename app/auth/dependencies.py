from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.user.models import User, UserRoles
from auth.services import AuthService

# Swagger UI'da Avtorizatsiya oynasi ochilishi uchun /auth/login manziliga yo'naltiramiz
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """
    Sarlavhadagi (Header) token orqali foydalanuvchini bazadan qidirib topadi.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token yaroqsiz yoki muddati o'tgan",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = AuthService.decode_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    # Modelingizdagi `User.username` va `User.is_active` orqali tekshiruv
    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Foydalanuvchi hisobi faol emas",
        )

    return user


class RoleChecker:
    """Rollar bo'yicha ruxsatlarni tekshiruvchi sinf."""

    def __init__(self, allowed_roles: list[UserRoles]):
        self.allowed_roles = allowed_roles

    def __call__(
        self, current_user: Annotated[User, Depends(get_current_user)]
    ) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sizda ushbu amalni bajarish uchun ruxsat yetarli emas!",
            )
        return current_user


# Boshqa app'larda (post, category, comment) ishlatiladigan ruxsatnomalar:
require_admin = RoleChecker([UserRoles.ADMIN])
require_author_or_admin = RoleChecker([UserRoles.ADMIN, UserRoles.AUTHOR])
require_any_user = RoleChecker([UserRoles.ADMIN, UserRoles.AUTHOR, UserRoles.USER])
