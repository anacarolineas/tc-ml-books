from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core import get_db, get_current_user
from src.schemas import StatsOverviewResponse, StatsCategoriesResponse, UserResponse
from src.crud import get_stats_overview, get_stats_categories

router = APIRouter()

@router.get(
        "/overview", 
        response_model=StatsOverviewResponse, 
        summary="Get general book statistics"
)
async def read_stats_overview(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)):
    """
    Returns an overview of book statistics.
    
    - Contains the total number of books.
    - Average price of books.
    - Distribution of books by rating.
    """
    return get_stats_overview(db=db)

@router.get(
        "/categories", 
        response_model=List[StatsCategoriesResponse], 
        summary="Get general category statistics"
    )
async def read_stats_categories(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)):
    """
    Returns an overview of category statistics.
    
    - Contains the total number of books per category.
    - Average price of books per category.
    """
    return get_stats_categories(db=db)