from fastapi import FastAPI
from app.database import engine, Base
from app.routes import author
from app.models.author import Author
from app.routes import book
from app.models.book import Book
from app.routes import review
from app.models.review import Review
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