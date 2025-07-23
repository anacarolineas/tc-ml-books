from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from src.core import get_current_user, get_db
from src.schemas import BookFeaturesResponse, UserResponse
from src.crud import get_book_by_id

router = APIRouter()

@router.get(
    "/ml/features/{book_id}",
    response_model=BookFeaturesResponse,
    summary="Get features of a book",
)
async def get_ml_features_for_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Endpoint to retrieve machine learning features.
    """
    book = get_book_by_id(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book