from fastapi import APIRouter,Depends,Path
from sqlalchemy.orm import Session
from starlette import status
from dependencies import get_db,get_current_user
from services.user_book import UserBookService,DetailResponse


router = APIRouter(
    tags=['user_book']
)

@router.post("/request-book", status_code = status.HTTP_201_CREATED)
async def request_book(data :dict,user: dict = Depends(get_current_user),db: Session = Depends(get_db)):
    user_book_service = UserBookService(db)
    return user_book_service.request_book(user,data)

@router.get("/pending-books", status_code = status.HTTP_200_OK)
async def pending_books(user: dict = Depends(get_current_user),db: Session = Depends(get_db)):
    user_book_service = UserBookService(db)
    return user_book_service.pending_books(user)

@router.put("/accept-book/{id}", status_code=status.HTTP_200_OK,response_model=DetailResponse)
async def accept_book_request(user: dict = Depends(get_current_user),db: Session = Depends(get_db),id: int = Path(gt=0)):
    print(id)
    user_book_service = UserBookService(db)
    return user_book_service.accept_book_request(user,id)

@router.put("/reject-book/{id}", status_code=status.HTTP_200_OK,response_model=DetailResponse)
async def accept_book_request(user: dict = Depends(get_current_user),db: Session = Depends(get_db),id: int = Path(gt=0)):
    print(id)
    user_book_service = UserBookService(db)
    return user_book_service.reject_book_request(user,id)