from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.book import Book
from schemas.book import BookCreate, BookResponse
from models.author import Author

router = APIRouter()
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(
        title= book.title,
        author_id = book.author_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/")
def get_books(db : Session = Depends(get_db)):
    data = (
        db.query(Book,Author)
        .join(Author, Book.author_id == Author.id).all()
    )
    return [
        {
            "id": b.id,
            "title": b.title,
            "author": a.name
        }
        for b,a in data
    ]