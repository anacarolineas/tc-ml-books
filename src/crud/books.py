from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from ..core.pagination import paginate
from ..schemas.page import Page
from ..models.book import Book
from ..models.category import Category

def get_books(db: Session, page: int, page_size: int = 50) -> Page:
    """
    Get all list of books from the database.
    
    :param db: Database session
    :return: List of books
    """
    books_query = db.query(Book).options(joinedload(Book.category))
    return paginate(books_query, page=page, page_size=page_size)

def get_book_by_id(db: Session, book_id: int) -> Book | None:
    """
    Get a book by its ID from the database.
    
    :param db: Database session
    :param book_id: ID of the book to retrieve
    :return: Book object if found, else None
    """
    return (
        db.query(Book)
        .filter(Book.id == book_id)
        .options(joinedload(Book.category))
        .first()
    )

def search_books(db: Session, title: str, category: str, page: int, page_size: int = 50) -> Page:
    """
    Search for books by title or category.
    
    :param db: Database session
    :param title: Title to filter books
    :param category: Category to filter books
    :param page: Page number for pagination
    :param page_size: Number of items per page
    :return: Paginated list of books matching the title or category
    """
    filters = []

    if title:
        filters.append(Book.title.ilike(f"%{title}%"))
    if category:
        filters.append(Category.name.ilike(f"%{category}%"))

    books_query = (
        db.query(Book)
        .join(Book.category)
        .options(joinedload(Book.category)))

    if filters:
        books_query = books_query.filter(or_(*filters))

    books_query = (
        db.query(Book)
        .join(Book.category)
        .filter(*filters)
        .options(joinedload(Book.category))
    )
    return paginate(books_query, page=page, page_size=page_size)

