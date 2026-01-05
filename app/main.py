from fastapi import FastAPI
from app.api.routers import books

app = FastAPI(title="Platform Buku online")

app.include_router(books.router, prefix="/books", tags=["books"])

@app.get("/")
def root():
    return {"message": "Platform Buku siap"}