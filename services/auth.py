from models.users import Users
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes = ['bcrypt'],deprecated = 'auto')

class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str

class AuthService:
    def __init__(self,db: Session):
        self.db = db

    def create_user(self,user:CreateUserRequest):
        create_user_model = Users(
        name = user.name,
        email = user.email,
        password =bcrypt_context.hash(user.password),
        is_admin = False
        )
        self.db.add(create_user_model)
        self.db.commit()

