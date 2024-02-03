from fastapi import APIRouter,Depends,Form
from sqlalchemy.orm import Session
from starlette import status
from dependencies import get_db,get_current_user
from services.books import BookService,BookRequest

router = APIRouter(
    tags=['books']
)

@router.post("/add-book", status_code = status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest,user: dict = Depends(get_current_user),db: Session = Depends(get_db)):
    book_service = BookService(db)
    return book_service.create_book(user,book_request)
