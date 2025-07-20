from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.stats import StatsOverviewResponse, StatsCategoriesResponse
from src.crud.stats import get_stats_overview, get_stats_categories

router = APIRouter()

@router.get("/stats/overview", response_model=StatsOverviewResponse, summary="Obter estatísticas gerais dos livros")
async def read_stats_overview(db: Session = Depends(get_db)):
    """
    Retorna uma visão geral das estatísticas dos livros.
    
    - Contém o número total de livros.
    - Preço médio dos livros.
    - Distribuição de livros por classificação.
    """
    return get_stats_overview(db=db)

@router.get("/stats/categories", response_model=List[StatsCategoriesResponse], summary="Obter estatísticas gerais das categorias")
async def read_stats_categories(db: Session = Depends(get_db)):
    """
    Retorna uma visão geral das estatísticas das categorias.
    
    - Contém o número total de livros por categoria.
    - Preço médio dos livros por categoria.
    """
    return get_stats_categories(db=db)