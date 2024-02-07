from pydantic import BaseModel
from pydantic import BaseModel,Field

class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str

class UserData(BaseModel):
    email: str
    password: str

class BookRequest(BaseModel):
    title: str
    description: str
    author: str
    image: str
    launched: str
    rating: int = Field(gt=0, lt=6)    

class DetailResponse(BaseModel):
    details: str    