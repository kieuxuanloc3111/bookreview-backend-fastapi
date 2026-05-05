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
@router.delete("/")
def delete_all_authors(db: Session = Depends(get_db)):
    count = db.query(Author).count()

    db.query(Author).delete()
    db.commit()

    return {"message": f"Deleted {count} authors"}
@router.delete("/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    db.delete(author)
    db.commit()

    return {"message": "Author deleted"}