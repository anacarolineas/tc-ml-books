
from fastapi import APIRouter, Depends, Query
from requests import Session
from src.core import get_current_user, get_db
from src.schemas import CategoryResponse, Page
from src.crud import get_categories
from src.schemas import UserResponse

router = APIRouter()

@router.get(
    "/", 
    response_model=Page[CategoryResponse], 
    summary="List all categories"
)
async def read_categories(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number to be returned"),
    page_size: int = Query(50, ge=1, le=1000, description="Number of items per page (maximum 1000)")
):
    """
    Retorna uma lista de todas as categorias disponíveis.
    
    - Cada categoria contém seu ID e nome.
    """

    return get_categories(db=db, page=page, page_size=page_size)