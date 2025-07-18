from fastapi import FastAPI
from src.api import books

app = FastAPI(
    title="Books To Scrape API",
    description="Uma API para analisar livros do Book To Scrape.",
    version="1.0.0"
)

app.include_router(
    books.router, 
    prefix="/api/v1",
    tags=["Livros"])