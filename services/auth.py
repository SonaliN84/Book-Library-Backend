from models.users import Users
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi import HTTPException
from starlette import status
from datetime import timedelta, datetime
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

bcrypt_context = CryptContext(schemes = ['bcrypt'],deprecated = 'auto')

class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str

class UserData(BaseModel):
    email: str
    password: str

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(user_id:int,expires_delta:timedelta):
    encode = {'id': user_id}
    expires=datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)    

class AuthService:
    def __init__(self,db: Session):
        self.db = db

    def create_user(self,user:CreateUserRequest):
        get_user =self.db.query(Users).filter(Users.email == user.email).first()
        if get_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exist!!")
        create_user_model = Users(
        name = user.name,
        email = user.email,
        password =bcrypt_context.hash(user.password),
        is_admin = False
        )
        self.db.add(create_user_model)
        self.db.commit()

    def login_user(self,user_data:UserData):
        user =self.db.query(Users).filter(Users.email == user_data.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user.')
        if not bcrypt_context.verify(user_data.password,user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Incorrect password')
        
        token = create_access_token(user.id,timedelta(days=1))
        return {'access_token':token,'is_Admin':user.is_admin}