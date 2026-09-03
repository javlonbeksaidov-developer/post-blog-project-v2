from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.services import AuthService

from .models import User, UserRoles
from .schemas import AdminCreate, UserCreate, UserPatch, UserUpdate


class UserService:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Foydalanuvchi topilmadi",
            )
        return user

    @staticmethod
    def create(db: Session, user_in: UserCreate) -> User:
        # Username yoki Email mavjudligini tekshirish
        existing_user = (
            db.query(User)
            .filter((User.username == user_in.username) | (User.email == user_in.email))
            .first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ushbu username yoki email allaqachon ro'yxatdan o'tgan",
            )

        hashed_pwd = AuthService.get_password_hash(user_in.password)
        new_user = User(
            username=user_in.username,
            email=user_in.email,
            password=hashed_pwd,
            full_name=user_in.full_name,
            role=UserRoles.USER,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def create_admin(db: Session, user_in: AdminCreate) -> User:
        # Username yoki Email mavjudligini tekshirish
        existing_user = (
            db.query(User)
            .filter((User.username == user_in.username) | (User.email == user_in.email))
            .first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ushbu username yoki email allaqachon ro'yxatdan o'tgan",
            )

        hashed_pwd = AuthService.get_password_hash(user_in.password)
        new_user = User(
            username=user_in.username,
            email=user_in.email,
            password=hashed_pwd,
            full_name=user_in.full_name,
            role=UserRoles.ADMIN,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def update_full(db: Session, user_id: int, user_in: UserUpdate) -> User:
        user = UserService.get_by_id(db, user_id)

        user.username = user_in.username
        user.email = user_in.email
        user.full_name = user_in.full_name
        user.role = user_in.role
        user.is_active = user_in.is_active

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_partial(db: Session, user_id: int, user_in: UserPatch) -> User:
        user = UserService.get_by_id(db, user_id)

        # Faqat yuborilgan (None bo'lmagan) maydonlarni yangilaymiz
        update_data = user_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: int):
        user = UserService.get_by_id(db, user_id)
        db.delete(user)
        db.commit()
        return {"messaage": "deleted user!"}
