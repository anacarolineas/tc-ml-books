from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db 
from ..schemas.book import BookResponse
from src.crud.books import get_books

router = APIRouter()

@router.get("/books", response_model=List[BookResponse], summary="Listar todos os livros")
async def read_books(db: Session = Depends(get_db)):
    """
    Retorna uma lista de livros com seus detalhes e categoria.

    - Cada livro contém seus detalhes completos.
    - A categoria associada a cada livro também é incluída.
    """
    return get_books(db=db)