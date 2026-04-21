from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.review import Review
from schemas.review import ReviewCreate, ReviewResponse
from models.book import Book
from models.author import Author

router = APIRouter()
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    new_review = Review(
        content= review.content,
        book_id = review.book_id
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.get("/")
def get_reviews(db : Session = Depends(get_db)):
    data = (
        db.query(Review, Book, Author)
        .join(Book, Review.book_id == Book.id)
        .join(Author, Book.author_id == Author.id).all()
    )
    return [
        {
            "id": r.id,
            "book"  : b.title,
            "author": a.name,
            "content": r.content
        }
        for r,b,a in data
    ]