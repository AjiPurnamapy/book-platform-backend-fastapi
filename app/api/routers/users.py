from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.db import get_session
from app.core.security import get_password_hashed, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    # menggunakan scalar yg langsung return object(bukan result object)
    existing_user = await session.scalar(
        select(User).where(User.email == user_in.email).limit(1)
    )

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

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):

    user = await session.scalar(
        select(User).where(User.email == form_data.username).limit(1)
    )
    
    # validasi user ada dan validasi pw cocok/tidak
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email atau password salah",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # buatkan token
    access_token = create_access_token(subject=user.id)

    return{
        "access_token": access_token,
        "token_type": "Bearer"
    }