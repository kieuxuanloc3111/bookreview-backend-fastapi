from pydantic import BaseModel
class AuthorCreate(BaseModel):
    name:str

class AuthorResponse(BaseModel):
    id:int
    name:str

    class Config:
        from_attributes = True