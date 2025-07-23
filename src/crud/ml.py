from typing import Iterator
from requests import Session
from src.models.book import Book

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