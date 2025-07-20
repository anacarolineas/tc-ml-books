
from fastapi import APIRouter, Depends, Query
from requests import Session
from src.schemas import CategoryResponse, Page
from src.core import get_db 
from src.crud import get_categories

router = APIRouter()

@router.get("/categories", response_model=Page[CategoryResponse], summary="Listar todas as categorias")
async def read_categories(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Número da página a ser retornada"),
    page_size: int = Query(50, ge=1, le=1000, description="Número de itens por página (máximo 1000)")
):
    """
    Retorna uma lista de todas as categorias disponíveis.
    
    - Cada categoria contém seu ID e nome.
    """

    return get_categories(db=db, page=page, page_size=page_size)