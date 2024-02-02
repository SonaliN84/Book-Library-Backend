from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")


SQLALCHEMY_DATABASE_URL=f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@127.0.0.1:3306/BookLibraryApplicationDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False ,autoflush=False,bind=engine)

Base = declarative_base()