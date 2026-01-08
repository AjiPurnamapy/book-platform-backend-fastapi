from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.db import get_session
from app.core.security import get_password_hashed
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    query = select(User).where(User.email == user_in.email)
    result = await session.execute(query)
    existing_user = result.first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email sudah terdaftar, silahkan gunakan email yang lain"
        )
    
    hashed_pw = get_password_hashed(user_in.password)

    new_user = User(
        email=user_in.email,
        hashed_password=hashed_pw,
        is_active=True
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user