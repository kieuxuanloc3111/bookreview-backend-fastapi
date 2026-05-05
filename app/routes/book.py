from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.book import Book
from app.schemas.book import BookCreate, BookResponse
from app.models.author import Author

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

@router.delete("/")
def delete_all_books(db: Session = Depends(get_db)):
    count = db.query(Book).count()

    db.query(Book).delete()
    db.commit()

    return {"message": f"Deleted {count} books"}


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()

    return {"message": "Book deleted"}