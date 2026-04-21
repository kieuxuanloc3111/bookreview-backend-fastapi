from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
