from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from requests import Session
from src.core import get_current_user, get_db, format_as_json_lines_training_data
from src.schemas import BookFeaturesResponse, UserResponse, BookTrainingDataResponse, PredictionResponse, BookResponse, PredictionCreate
from src.crud import get_book_by_id, stream_training_data, save_prediction

router = APIRouter()

@router.get(
    "/features/{book_id}",
    response_model=BookFeaturesResponse,
    summary="Get features of a book",
)
async def get_ml_features_for_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
) -> BookResponse:
    """
    Endpoint to retrieve machine learning features.
    """
    book = get_book_by_id(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@router.get(
    "/training-data",
    summary="Stream all books training data"
)
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

@router.post(
    "/predictions",
    response_model=PredictionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a prediction for a book"
)
async def create_prediction(
    payload: PredictionCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
) -> PredictionResponse:
    """
    Endpoint to save a prediction for a book.
    """
    prediction = save_prediction(
        db=db,
        book_id=payload.book_id,
        predicted_price=payload.predicted_price,
        model_version=payload.model_version
    )
    return PredictionResponse.model_validate(prediction)

