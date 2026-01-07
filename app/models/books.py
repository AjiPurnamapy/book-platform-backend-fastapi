from sqlmodel import SQLModel, Field
from typing import Optional

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author: str = Field(min_length=1, max_length=255)
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    price: int 
