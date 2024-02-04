from fastapi import HTTPException
from pydantic import BaseModel,Field
from models.books import Books
from starlette import status
from sqlalchemy.orm import Session

class BookRequest(BaseModel):
    title: str
    description: str
    author: str
    image: str
    launched: str
    rating: int = Field(gt=0, lt=6)
    quantity: int = Field(gt=-1)

class BookService:
    def __init__(self,db: Session):
        self.db = db

    def create_book(self,user: dict,book:BookRequest):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
        get_book =self.db.query(Books).filter(Books.title == book.title).first()
        if get_book:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Book already exist!!")
    
        create_book_model = Books(**book.dict(),availability=book.quantity)
        self.db.add(create_book_model)
        self.db.commit()    

    def get_books(self,user: dict):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')  
        return self.db.query(Books).all(); 