from fastapi import FastAPI
from src.api import books, categories, health, stats

app = FastAPI(
    title="Books To Scrape API",
    description="Uma API para analisar livros do Book To Scrape.",
    version="1.0.0"
)

app.include_router(
    books.router, 
    prefix="/api/v1",
    tags=["Livros"])

app.include_router(
    categories.router, 
    prefix="/api/v1",
    tags=["Categorias"])

app.include_router(
    stats.router, 
    prefix="/api/v1",
    tags=["Stats"])

app.include_router(
    health.router, 
    prefix="/api/v1",
    tags=["Health"])
