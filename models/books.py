from database import Base
from sqlalchemy import Column,Integer,String,DateTime

class Books(Base):
    __tablename__ ='books'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(255),unique=True)
    author = Column(String(255))
    image = Column(String(255))
    description = Column(String(255))
    rating = Column(Integer)
    launched = Column(DateTime)
    quantity = Column(Integer)
    availability = Column(Integer)
