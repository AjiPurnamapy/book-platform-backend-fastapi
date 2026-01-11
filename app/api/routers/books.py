from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.books import BookCreate, BookResponse, BookUpdate
from app.core.db import get_session
from app.models.books import Book
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=BookResponse)
async def create_books(
    book_in: BookCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create new book
    """
    new_book = Book.model_validate(book_in)
    new_book.user_id = current_user.id

    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)

    return new_book

@router.get("/", response_model=List[BookResponse])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    skip: int = 0, limit: int = 100
):
    query = select(Book).offset(skip).limit(limit)
    result = await session.execute(query)
    books = result.scalars().all()

    return books

@router.get("/{book_id}")
async def read_book_by_id(
    book_id: int,
    session: AsyncSession = Depends(get_session),
):
    """
    Get book by ID
    """
    book = await session.get(Book, book_id)

    if not book :
        raise HTTPException(status_code=404, detail="Buku tidak ditemukan!")
    
    return book

@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_update: BookUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update a book
    """
    db_book = await session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
    
    if db_book.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tidak cukup hak akses untuk mengubah buku ini",
        )
    
    book_data = book_update.model_dump(exclude_unset=True)
    db_book.sqlmodel_update(book_data)

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    return db_book

@router.delete("/{book_id}")
async def delete(
    book_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a book
    """
    db_book = await session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
    
    if db_book.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda bukan pemilik buku ini",
        )
    
    await session.delete(db_book)
    await session.commit()

    return {"message": "Buku berhasil dihapus"}