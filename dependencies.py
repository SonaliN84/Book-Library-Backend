from database import SessionLocal
from jose import jwt,JWTError
from dotenv import load_dotenv
import os
from fastapi.security import  OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from starlette import status
from typing import Annotated

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
     try:
         print("token "+token)
         payload =jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
         print("payload",payload)
         user_id:int =payload.get('id')
         if user_id is None:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user.')
         return {'user_id':user_id}
     except JWTError:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')