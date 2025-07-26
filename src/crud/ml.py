from typing import Iterator
from requests import Session
from src.models import Book, Prediction

BATCH_SIZE = 1000

def stream_training_data(db: Session) -> Iterator[Book]:
    """
    Fetches all books from the database and returns them as a stream
    to avoid excessive memory usage.
    """
    # Search by batch of 1000
    query = db.query(Book).yield_per(BATCH_SIZE)
    for book in query:
        yield book

def save_prediction(db: Session, book_id: int, predicted_price: float, model_version: str) -> Prediction:
    """
    Saves a prediction to the database.
    """
    prediction = Prediction(
        book_id=book_id,
        predicted_price=predicted_price,
        model_version=model_version
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction