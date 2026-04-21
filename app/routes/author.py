from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorResponse

router = APIRouter()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    new_author = Author(name=author.name)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

@router.get("/")
def get_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()