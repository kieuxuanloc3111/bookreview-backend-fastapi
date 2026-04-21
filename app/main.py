from fastapi import FastAPI
from database import engine, Base
from routes import author
from models.author import Author
from routes import book
from models.book import Book
from routes import review
from models.review import Review
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(author.router, prefix="/authors", tags=["Authors"])
app.include_router(book.router, prefix="/books", tags=["Books"])
app.include_router(review.router, prefix="/reviews", tags=["Reviews"])