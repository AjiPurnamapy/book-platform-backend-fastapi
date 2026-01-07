from sqlmodel import SQLModel, Field
from typing import Optional

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author: str
    title: str
    description: Optional[str] = None
    price: float
