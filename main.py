from fastapi import FastAPI
from src.core import limiter
from src.middlewares.logging_middleware import structured_logging_middleware
from src.api import books, categories, health, stats, auth, user, ml
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI(
    title="Books To Scrape API",
    description="Uma API para analisar livros do Book To Scrape.",
    version="1.0.0"
)

# Configure rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
    prefix="/api/v1/books",
    tags=["Books"])

app.include_router(
    categories.router, 
    prefix="/api/v1/categories",
    tags=["Categories"])

app.include_router(
    stats.router, 
    prefix="/api/v1/stats",
    tags=["Stats"])

app.include_router(
    ml.router, 
    prefix="/api/v1/ml",
    tags=["Machine Learning"])

app.include_router(
    health.router, 
    prefix="/api/v1",
    tags=["Health"])
