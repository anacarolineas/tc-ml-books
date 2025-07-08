# main.py
from fastapi import FastAPI

# Cria a instância da aplicação
app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "API rodando com FastAPI e uv!"}
