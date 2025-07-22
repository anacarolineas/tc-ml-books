from fastapi import FastAPI
from src.middlewares.logging_middleware import structured_logging_middleware
from src.api import books, categories, health, stats, auth, user

app = FastAPI(
    title="Books To Scrape API",
    description="Uma API para analisar livros do Book To Scrape.",
    version="1.0.0"
)

app.middleware("http")(structured_logging_middleware)

app.include_router(
    auth.router, 
    prefix="/api/v1",
    tags=["Auth"])

app.include_router(
    user.router, 
    prefix="/api/v1",
    tags=["Users"])

app.include_router(
    books.router, 
    prefix="/api/v1",
    tags=["Books"])

app.include_router(
    categories.router, 
    prefix="/api/v1",
    tags=["Categories"])

app.include_router(
    stats.router, 
    prefix="/api/v1",
    tags=["Stats"])

app.include_router(
    health.router, 
    prefix="/api/v1",
    tags=["Health"])
