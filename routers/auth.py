from fastapi import APIRouter,Depends
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel
from models.users import Users
from dependencies import get_db
from services.auth import AuthService,CreateUserRequest


router = APIRouter(
    tags=['auth']
)

@router.post("/signup", status_code = status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest,db: Session = Depends(get_db)):
    
    auth_service = AuthService(db)
    return auth_service.create_user(create_user_request)



    
