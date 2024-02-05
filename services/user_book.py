from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user_book import UserBook
from models.books import Books
from models.users import Users
from sqlalchemy import select
from pydantic import BaseModel

class DetailResponse(BaseModel):
    details: str

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
        
        db_user_book = self.db.query(UserBook).filter(UserBook.user_id == user.get('id')).filter(UserBook.book_id == data.get('book_id')).first()
        
        if db_user_book is not None:
            if db_user_book.status == "Pending":
                raise HTTPException(status_code=400, detail="Book already requested!!") 

            if db_user_book.status == "Issued":
                raise HTTPException(status_code=400, detail="Book already issued!!")  
        
        user_book_data=UserBook(user_id=user.get('id'), book_id=data.get('book_id'), status="Pending")
        self.db.add(user_book_data)
        self.db.commit()
       
    def pending_books(self,user:dict):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
        
        # SELECT user_book.user_id, user_book.book_id, user_book.status, users.name, books.title 
        # FROM user_book JOIN users ON users.id = user_book.user_id JOIN books ON books.id = user_book.book_id 
        # WHERE user_book.status = :status_1

        query = select(UserBook.id,UserBook.user_id, UserBook.book_id, UserBook.status, Users.name,Users.email, Books.title,Books.image,Books.author).\
            join(Users).join(Books).where(UserBook.status == 'Pending')
        print(query)
        result = self.db.execute(query).fetchall()
        print(result)

        response = []
        for id, user_id, book_id, status, username, email, title, image,  author in result:
            response.append({
                "id":id,
                "user_id": user_id,
                "book_id": book_id,
                "status": status,
                "username": username,
                "useremail":email,
                "book_title": title,
                "book_image":image,
                "book_author":author
            })

        return response

    def accept_book_request(self,user:dict,id:int):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
        
        data = self.db.query(UserBook).filter(UserBook.id == id).first()

        if data.status == 'Issued':
            return {"details":"Book already issued!!"}
        
        if data.status == "Pending":
            book = self.db.query(Books).filter(Books.id == data.book_id).first()

            if book.availability <= 0:
                raise HTTPException(status_code=400, detail='Book is out of stock...can not issue!!')

            # student validation

            book.availability = book.availability - 1
            print(book.availability)
            data.status = "Issued"
            print(data.status)
            self.db.add(data)
            self.db.add(book)
            self.db.commit()
            
            return { "details":"Book issued successfully"}
         


