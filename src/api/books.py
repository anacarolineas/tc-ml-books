from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..schemas.page import Page
from ..database import get_db 
from ..schemas.book import BookResponse
from src.crud.books import get_books, get_book_by_id, search_books, get_books_top_rated, get_books_by_price_range

router = APIRouter()

@router.get("/books", response_model=Page[BookResponse], summary="Listar todos os livros")
async def read_books(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Número da página a ser retornada"),
    page_size: int = Query(50, ge=1, le=1000, description="Número de itens por página (máximo 1000)")
):
    """
    Retorna uma lista de livros com seus detalhes e categoria.

    - Cada livro contém seus detalhes completos.
    - A categoria associada a cada livro também é incluída.
    """
    return get_books(db=db, page=page, page_size=page_size)

@router.get("/books/price-range", response_model=Page[BookResponse], summary="Listar livros por faixa de preço  entre dois valores  mínimo e máximo de preço")
async def read_books_by_price_range(
    min_price: float = Query(..., description="Preço mínimo para filtrar livros"),
    max_price: float = Query(..., description="Preço máximo para filtrar livros"),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Número da página a ser retornada"),
    page_size: int = Query(50, ge=1, le=1000, description="Número de itens por página (máximo 1000)")
):
    """
    Retorna uma lista de livros filtrados por faixa de preço.

    - `min_price`: Preço mínimo para filtrar os livros.
    - `max_price`: Preço máximo para filtrar os livros.
    - Retorna uma lista paginada de livros que estão dentro da faixa de preço especificada.
    """
    return get_books_by_price_range(db=db, min_price=min_price, max_price=max_price, page=page, page_size=page_size)

@router.get("/books/top-rated", response_model=Page[BookResponse], summary="Listar livros mais bem avaliados. Nota maior ou igual a 4")
async def read_top_rated_books(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Número da página a ser retornada"),
    page_size: int = Query(50, ge=1, le=1000, description="Número de itens por página (máximo 1000)")
):
    """
    Retorna uma lista de livros mais bem avaliados. Nota maior ou igual a 4

    - Cada livro contém seus detalhes completos.
    - A categoria associada a cada livro também é incluída.
    """
    return get_books_top_rated(db=db, page=page, page_size=page_size)

@router.get("/books/search", response_model=Page[BookResponse], summary="Pesquisar livros por título ou categoria")
async def search(
    title: str = Query("", description="Título do livro para pesquisa"),
    category: str = Query("", description="Categoria do livro para pesquisa"),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Número da página a ser retornada"),
    page_size: int = Query(50, ge=1, le=1000, description="Número de itens por página (máximo 1000)")
):
    """
    Pesquisa livros por título ou categoria.

    - `title`: Título do livro para filtrar os resultados.
    - `category`: Categoria do livro para filtrar os resultados.
    - Retorna uma lista paginada de livros que correspondem aos critérios de pesquisa.
    """
    return search_books(db=db, title=title, category=category, page=page, page_size=page_size)

@router.get("/books/{book_id}", response_model=BookResponse, summary="Obter detalhes de um livro específico")
async def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retorna os detalhes de um livro específico, incluindo sua categoria.

    - `book_id`: ID do livro a ser consultado.
    - Retorna os detalhes completos do livro e sua categoria associada.
    """
    book = get_book_by_id(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book



