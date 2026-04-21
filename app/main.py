from fastapi import FastAPI
from database import engine, Base
from routes import author
from models.author import Author
from routes import book
from models.book import Book
from routes import review
from models.review import Review
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(author.router, prefix="/authors", tags=["Authors"])
app.include_router(book.router, prefix="/books", tags=["Books"])
app.include_router(review.router, prefix="/reviews", tags=["Reviews"])