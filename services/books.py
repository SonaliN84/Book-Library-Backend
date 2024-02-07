from fastapi import HTTPException
from models.books import Books
from starlette import status
from sqlalchemy.orm import Session
from models.user_book import UserBook
from models.books import Books
from models.users import Users
from sqlalchemy import select,and_
from schema.schema import BookRequest

class BookService:
    def __init__(self,db: Session):
        self.db = db

    def create_book(self,user: dict,book:BookRequest):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
        get_book =self.db.query(Books).filter(Books.title == book.title).first()
        if get_book:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Book already exist!!")
    
        create_book_model = Books(**book.dict())
        self.db.add(create_book_model)
        self.db.commit()    

    def get_books(self,user: dict,page:int,size:int):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')  
        skip = (page - 1) * size
        total= self.db.query(Books).count()

        books= self.db.query(Books).offset(skip).limit(size).all(); 
        return { "total":total,"books":books}

    def get_my_books(self,user:dict):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed') 
        
        # SELECT user_book.id, books.title, books.image, books.author, books.launched 
        # FROM user_book JOIN books ON books.id = user_book.book_id 
        # WHERE user_book.status = :status_1 AND user_book.user_id = :user_id_1

        query = select(UserBook.id,UserBook.issued_date,Books.title,Books.image,Books.author).\
            join(Books).where(and_(UserBook.status == 'Issued',UserBook.user_id == user.get('id')))
        print(query)
        result = self.db.execute(query).fetchall()
        print(result)

        response = []
        for id, issued_date,title, image, author in result:
            response.append({
                "id":id,
                "title": title,
                "image":image,
                "author":author,
                "issued_date":issued_date
            })

        return response
    
    def get_book_detail(self,user:dict,book_id:int):
       if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed') 

       book_pending = self.db.query(UserBook).filter(UserBook.user_id == user.get("id")).filter(UserBook.book_id == book_id).filter(UserBook.status == 'Pending').first()
       book_issued = self.db.query(UserBook).filter(UserBook.user_id == user.get("id")).filter(UserBook.book_id == book_id).filter(UserBook.status == 'Issued').first()

       if book_issued is not None or book_pending is not None:
          raise HTTPException(status_code=400, detail='Book already requested or issued!')

    def get_books_by_status(self,user:dict,status:str):
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed') 
        
        # SELECT user_book.id, books.title, books.image, books.author, books.launched 
        # FROM user_book JOIN books ON books.id = user_book.book_id 
        # WHERE user_book.status = :status_1 AND user_book.user_id = :user_id_1

        query = select(UserBook.id,UserBook.return_date,Books.title,Books.image,Books.author).\
            join(Books).where(and_(UserBook.status == status,UserBook.user_id == user.get('id')))
        print(query)
        result = self.db.execute(query).fetchall()
        print(result)

        response = []
        for id,return_date, title, image, author in result:
            response.append({
                "id":id,
                "title": title,
                "image":image,
                "author":author,
                "return_date":return_date
            })

        return response
