from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    description: str


class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        from_attributes = True
