from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.security import ALGORITHM, SECRET_KEY
from app.models.user import User
from app.schemas.user import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception
        
        token_data = TokenData(id=int(user_id))

    except JWTError:
        raise credentials_exception
    
    user = await session.get(User, token_data.id)

    if user is None:
        raise credentials_exception
    
    return user