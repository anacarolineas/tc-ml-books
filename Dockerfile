FROM python:3.12-slim

RUN pip install uv
WORKDIR /app
COPY pyproject.toml .
RUN uv pip sync --no-cache pyproject.toml
COPY . .
ENV DATABASE_URL=sqlite:////data/books_toscrape.db

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]