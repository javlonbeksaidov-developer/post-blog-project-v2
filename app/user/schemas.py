from datetime import datetime

from pydantic import BaseModel, EmailStr

from .models import UserRoles


# Yaratishda (POST) kiritiladigan ma'lumotlar
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    role: UserRoles = UserRoles.USER


# To'liq yangilashda (PUT) kiritiladigan ma'lumotlar
class UserUpdate(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: UserRoles
    is_active: bool


# Qisman yangilashda (PATCH) kiritiladigan ma'lumotlar (Barchasi optional)
class UserPatch(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None
    role: UserRoles | None = None
    is_active: bool | None = None


# Parolni o'zgartirish uchun (PATCH)
class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str


# Javob qaytganda (GET, POST, PUT, PATCH) ishlatiladigan sxema (Parol qaytarilmaydi!)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    role: UserRoles
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
