
from typing import List
from requests import Session
from sqlalchemy import func
from ..models.category import Category
from ..schemas.stats import StatsCategoriesResponse
from ..schemas.stats import StatsOverviewResponse
from ..models.book import Book

def get_stats_overview(db: Session) -> StatsOverviewResponse:
    """
    Get an overview of the statistics for books in the database.
    
    :param db: Database session
    :return: Total books, average price and dictionary containing rating distribution
    """
    average_price = db.query(func.avg(Book.price)).scalar()
    total_books = db.query(Book).count()
    ratings_dist_raw = db.query(
        Book.rating, func.count(Book.id)
    ).group_by(Book.rating).all()
    rating_distribution = {rating.name: count for rating, count in ratings_dist_raw}

    return StatsOverviewResponse(
        total_books=total_books,
        average_price=round(average_price, 2),
        rating_distribution=rating_distribution)

def get_stats_categories(db: Session) -> List[StatsCategoriesResponse]:
    """
    Get the count of books per category.
    
    :param db: Database session
    :return: Dictionary with category names as keys and book counts as values
    """
    stats_raw = (
        db.query(
        Category.name,
        func.count(Book.id),
        func.avg(Book.price)
        )
        .join(Book.category)
        .group_by(Category.name).all()
    )

    return [
        StatsCategoriesResponse(
            category=category_name,
            total_books=book_count,
            average_price=round(avg_price, 2) if avg_price is not None else 0.0
        )
        for category_name, book_count, avg_price in stats_raw
    ]
