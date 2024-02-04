from database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,Date
from sqlalchemy.orm import relationship

class UserBook(Base): 

    __tablename__ = "user_book"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    status = Column(String(255))
    issued_date = Column(Date)
    return_date = Column(Date)

    users = relationship("Users", back_populates="books")
    books = relationship("Books", back_populates="users")
