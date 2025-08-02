FROM python:3.12

RUN pip install uv

WORKDIR /app

COPY pyproject.toml .
COPY . .

RUN uv venv && uv pip install . --no-cache-dir

ENV PATH="/app/.venv/bin:$PATH"
ENV DATABASE_URL=sqlite:///books_toscrape.db
ENV SECRET_KEY=your-default-super-secure-secret

RUN mkdir -p /data

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]