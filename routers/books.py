from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from starlette import status
from commons.dependencies import get_db,get_current_user
from services.books import BookService
from schema.schema import BookRequest

router = APIRouter(
    tags=['books']
)

@router.post("/add-book", status_code = status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest,user: dict = Depends(get_current_user),db: Session = Depends(get_db)):
    book_service = BookService(db)
    return book_service.create_book(user,book_request)

@router.get("/books", status_code = status.HTTP_200_OK)
async def get_books(user: dict = Depends(get_current_user),db: Session = Depends(get_db),page:int = Query(gt=0),size:int = Query(gt=0)):
    book_service = BookService(db)
    return book_service.get_books(user,page,size)

@router.get("/my-books",status_code=status.HTTP_200_OK)
async def get_my_books(user: dict =Depends(get_current_user), db:Session = Depends(get_db)):
    book_service = BookService(db)
    return book_service.get_my_books(user)


@router.get("/get-book-detail/{book_id}",status_code=status.HTTP_200_OK)
async def get_book_detail(book_id: int,user: dict =Depends(get_current_user), db:Session = Depends(get_db)):
    book_service = BookService(db)
    return book_service.get_book_detail(user,book_id)

@router.get("/book/{status}",status_code=status.HTTP_200_OK)
async def get_books_by_status(status: str,user: dict =Depends(get_current_user), db:Session = Depends(get_db)):
    book_service = BookService(db)
    return book_service.get_books_by_status(user,status)

