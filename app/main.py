from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db import init_db
from app.api.routers import books, users
from app.models import books as book_model
from app.models import user as user_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # mencoba connect dan buat tabel, saat server nyala
    print("Mencoba Koneksi database...")
    await init_db()
    print("Database berhasil connect & tabel dibuat!")
    yield
    # clean up resource saat server mati

app = FastAPI(title="Platform Buku online", lifespan=lifespan)

app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Platform Buku siap"}