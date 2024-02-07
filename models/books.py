from database import Base
from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.orm import relationship

class Books(Base):
    __tablename__ ='books'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(255),unique=True)
    author = Column(String(255))
    image = Column(String(255))
    description = Column(String(500))
    rating = Column(Integer)
    launched = Column(DateTime)

    users = relationship("UserBook", back_populates="books")
