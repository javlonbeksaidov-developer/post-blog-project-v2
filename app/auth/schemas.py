from pydantic import BaseModel


# Login muvaffaqiyatli bo'lganda qaytadigan token formati
class Token(BaseModel):
    access_token: str
    token_type: str


# JWT token dekod qilinganda uning ichidan chiqadigan ma'lumot
class TokenData(BaseModel):
    username: str | None = None
