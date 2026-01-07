from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr =  Field(unique=True, index=True, max_length=255)
    hashed_password: str 
    is_active: bool = Field(default=True)