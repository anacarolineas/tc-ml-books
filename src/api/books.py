from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import get_current_user
from src.schemas import Page, BookResponse, UserResponse
from src.crud import get_books, get_book_by_id, search_books, get_books_top_rated, get_books_by_price_range

router = APIRouter()

@router.get(
    "/", 
    response_model=Page[BookResponse], 
    summary="List all books"
)
async def read_books(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),  
    page: int = Query(1, ge=1, description="Page number to be returned"),
    page_size: int = Query(50, ge=1, le=1000, description="Number of items per page (maximum 1000)")
):
    """
    Returns a list of books with their details and category.

    - Each book contains its complete details.
    - The category associated with each book is also included.
    """
    return get_books(db=db, page=page, page_size=page_size)

@router.get(
    "/price-range", 
    response_model=Page[BookResponse], 
    summary="List books by price range between two values: minimum and maximum price"
)
async def read_books_by_price_range(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
    min_price: float = Query(..., description="Minimum price to filter books"),
    max_price: float = Query(..., description="Maximum price to filter books"),
    page: int = Query(1, ge=1, description="Page number to be returned"),
    page_size: int = Query(50, ge=1, le=1000, description="Number of items per page (maximum 1000)")
):
    """
    Returns a list of books filtered by price range.

    - `min_price`: Minimum price to filter books.
    - `max_price`: Maximum price to filter books.
    - Returns a paginated list of books within the specified price range.
    """
    return get_books_by_price_range(db=db, min_price=min_price, max_price=max_price, page=page, page_size=page_size)

@router.get(
    "/top-rated", 
    response_model=Page[BookResponse], 
    summary="List top-rated books. Rating greater than or equal to 4"
)
async def read_top_rated_books(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number to be returned"),
    page_size: int = Query(50, ge=1, le=1000, description="Number of items per page (maximum 1000)")
):
    """
    Returns a list of top-rated books. Rating greater than or equal to 4

    - Each book contains its complete details.
    - The category associated with each book is also included.
    """
    return get_books_top_rated(db=db, page=page, page_size=page_size)

@router.get(
    "/search", 
    response_model=Page[BookResponse], 
    summary="Search books by title or category"
)
async def search(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
    title: str = Query("", description="Book title for search"),
    category: str = Query("", description="Book category for search"),
    page: int = Query(1, ge=1, description="Page number to be returned"),
    page_size: int = Query(50, ge=1, le=1000, description="Number of items per page (maximum 1000)")
):
    """
    Search books by title or category.

    - `title`: Book title to filter results.
    - `category`: Book category to filter results.
    - Returns a paginated list of books matching the search criteria.
    """
    return search_books(db=db, title=title, category=category, page=page, page_size=page_size)

@router.get(
    "/{book_id}", 
    response_model=BookResponse, 
    summary="Get details of a specific book by ID"
)
async def read_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Returns the details of a specific book, including its category.

    - `book_id`: ID of the book to be retrieved.
    - Returns the complete details of the book and its associated category.
    """
    book = get_book_by_id(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book



