from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from requests import Session
from src.core import get_current_user, get_db, format_as_json_lines_training_data
from src.schemas import BookFeaturesResponse, UserResponse, BookTrainingDataResponse
from src.crud import get_book_by_id, stream_training_data

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

@router.get(
    "/ml/training-data",
    summary="Get features of a book")
async def get_ml_training_data(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Endpoint to retrieve training data for machine learning.
    """
    books_db_stream = stream_training_data(db)
    books_schema_stream = (BookTrainingDataResponse.model_validate(book) for book in books_db_stream)

    return StreamingResponse(
        content=format_as_json_lines_training_data(books_schema_stream),
        media_type="application/json"
    )

