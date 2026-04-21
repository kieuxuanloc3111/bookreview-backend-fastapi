from pydantic import BaseModel
class ReviewCreate(BaseModel):
    content:str
    book_id:int
class ReviewResponse(BaseModel):
    id:int
    content:str
    book_id:int

    class Config:
        from_attributes = True

        