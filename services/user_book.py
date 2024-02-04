from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user_book import UserBook
from models.books import Books
from models.users import Users

class UserBookService:
    def __init__(self,db: Session):
        self.db = db

    def request_book(self,user:dict,data :dict):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
    
        db_user = self.db.query(Users).filter(Users.id == user.get('id')).first()
        db_book = self.db.query(Books).filter(Books.id == data.get('book_id')).first()

        if db_user is None or db_book is None:
           raise HTTPException(status_code=404, detail="User or book not found")
        
        user_book_data=UserBook(user_id=user.get('id'), book_id=data.get('book_id'), status="Pending")
        self.db.add(user_book_data)
        self.db.commit()
       

         


