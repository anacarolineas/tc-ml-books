from typing import List
from requests import Session
from models.book import Book

def get_books(db: Session) -> List[Book]:
    """
    Get all list of books from the database.
    
    :param db: Database session
    :return: List of books
    """
    return db.query(Book).all()