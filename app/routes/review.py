from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewResponse
from app.models.book import Book
from app.models.author import Author

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
@router.delete("/")
def delete_all_reviews(db: Session = Depends(get_db)):
    count = db.query(Review).count()

    db.query(Review).delete()
    db.commit()

    return {"message": f"Deleted {count} reviews"}
@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()

    return {"message": "Review deleted"}