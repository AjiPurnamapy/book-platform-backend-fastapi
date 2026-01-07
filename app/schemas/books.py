from pydantic import BaseModel, ConfigDict,Field
from typing import Optional

class BooksCreate(BaseModel):
    author: str = Field(max_length=100)
    title: str = Field(max_length=500)
    description: str | None = None
    price: float = Field(ge=0)

class BooksResponse(BooksCreate):
    id: Optional[int] 

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    description: str | None = None
    price: float | None = None

configt_model = ConfigDict(from_attributes=True)