
from requests import Session
from src.core.pagination import paginate
from src.schemas import Page
from src.models import Category

def get_categories(db: Session, page: int, page_size: int = 50) -> Page:
    """
    Get all categories from the database.
    
    :param db: Database session
    :return: List of categories
    """
    categories_query = db.query(Category)
    return paginate(categories_query, page=page, page_size=page_size)