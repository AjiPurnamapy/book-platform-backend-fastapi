from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from pydantic import EmailStr

if TYPE_CHECKING:
    from app.models.books import Book

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr =  Field(unique=True, index=True, max_length=255)
    hashed_password: str 
    is_active: bool = Field(default=True)

    # relasi table, satu user punya banyak book
    # "owner" adalah nama variabel di table book
    books: List["Book"] = Relationship(back_populates="owner")