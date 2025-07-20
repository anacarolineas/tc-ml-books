from pydantic import BaseModel, Field
from typing import Dict

class StatsOverviewResponse(BaseModel):
    total_books: int = Field(..., description="Total number of books in the collection.")
    average_price: float = Field(..., description="Average price of a book.")
    rating_distribution: Dict[str, int] = Field(..., description="Distribution of books by rating.")

class StatsCategoriesResponse(BaseModel):
    category: str = Field(..., description="Category name.")
    total_books: int = Field(..., description="Number of books in the category.")
    average_price: float = Field(..., description="Average price of books in the category.")
