from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user_book import UserBook
from models.books import Books
from models.users import Users
from sqlalchemy import select
from datetime import datetime

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
        
        book_pending = self.db.query(UserBook).filter(UserBook.user_id == user.get("id")).filter(UserBook.book_id == data.get('book_id')).filter(UserBook.status == 'Pending').first()
        book_issued = self.db.query(UserBook).filter(UserBook.user_id == user.get("id")).filter(UserBook.book_id == data.get('book_id')).filter(UserBook.status == 'Issued').first()

        if book_issued is not None or book_pending is not None:
          raise HTTPException(status_code=400, detail='Book already requested or issued!')
 
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
            data.status = "Issued"
            data.issued_date = datetime.now()
            print(data.status)
            self.db.add(data)
            self.db.commit()
            
            return { "details":"Book issued successfully"}
         
    def reject_book_request(self,user:dict,id:int):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
        
        data = self.db.query(UserBook).filter(UserBook.id == id).first()
        if data.status == 'Pending' or data.status == 'Rejected':
            data.status = "Rejected"
            self.db.add(data)
            self.db.commit()
            return {"details":"Book request rejetced!"}
        if data.status == 'Issued':
            return {"details":"Sorry,other admin accepted the book issue request!"}  
          
    
    def return_book_request(self,user:dict,id:int):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
        
        data = self.db.query(UserBook).filter(UserBook.id == id).first()
        data.status = "Returned"
        data.return_date = datetime.now()
        self.db.add(data)
        self.db.commit()
        return {"details":"Book returned successfully"} 