from fastapi import APIRouter,Depends,Form
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from models.users import Users
from dependencies import get_db
from services.auth import AuthService,CreateUserRequest
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


router = APIRouter(
    tags=['auth']
)

@router.post("/signup", status_code = status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest,db: Session = Depends(get_db)):
    
    auth_service = AuthService(db)
    return auth_service.create_user(create_user_request)

@router.post("/login",status_code=status.HTTP_200_OK)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: Session = Depends(get_db)):

    auth_service = AuthService(db)
    return auth_service.login_user(form_data.username,form_data.password)

    
