from fastapi import APIRouter, HTTPException
from app.schemas.books import BooksCreate, BooksResponse
from typing import List

router = APIRouter()

book_db = []
current_id = 0

@router.post("/", response_model=BooksResponse)
def create_books(book_in: BooksCreate):
    global current_id
    current_id += 1
    new_book = book_in.model_dump()
    new_book["id"] = current_id
    book_db.append(new_book)
    return new_book

@router.get("/", response_model=List[BooksResponse])
def get_all_books():
    return book_db

@router.get("/{books_id}")
def get_books_by_id(books_id: int):
    for book in book_db:
        if book["id"] == books_id:
            return book
    raise HTTPException(status_code=404, detail="Bukut tidak ditemukan")
