from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class BookCreate(BaseModel):
    author: str = Field(min_length=1, max_length=255)
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1, max_length=1000) 
    price: int = Field(ge=0)

class BookUpdate(BaseModel):
    author: str | None = Field(default=None, min_length=1, max_length=255)
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    price: int | None = Field(ge=0)

class BookResponse(BookCreate):
    id: Optional[int] 

    model_config = ConfigDict(from_attributes=True)