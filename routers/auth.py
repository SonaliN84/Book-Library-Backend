from fastapi import APIRouter,Depends,Form
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from models.users import Users
from commons.dependencies import get_db
from services.auth import AuthService
from schema.schema import CreateUserRequest
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(
    tags=['auth']
)

@router.post("/signup", status_code = status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest,db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.create_user(create_user_request)

@router.post("/token",status_code=status.HTTP_200_OK)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.login_user(form_data) 

