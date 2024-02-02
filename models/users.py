from database import Base
from sqlalchemy import Column,Integer,String,Boolean

class Users(Base):
    __tablename__ ='users'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255))
    email = Column(String(255),unique=True)
    password = Column(String(255))
    is_admin = Column(Boolean,default=False)
