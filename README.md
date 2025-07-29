# TC ML Books

Uma API RESTful baseada em FastAPI para consulta de livros, categorias, previsões de machine learning e cadastro de usuários. 
Os dados disponíveis para essa API foram extraídos do site [books.toscrape](https://books.toscrape.com/).

## Funcionalidades

- 📚 Busca e filtragem de livros e suas categorias
- 👤 Autenticação de usuários (JWT)
- 📊 Endpoints de estatísticas (visão geral, categorias)
- 🤖 Endpoints de Machine Learning (features, dados de treino, previsões)
- 🩺 Endpoint de helth check
- 🖥️ Scraper de livros do site [books.toscrape](https://books.toscrape.com/)

## Tecnologias

- Python 3.12+
- FastAPI
- SQLAlchemy
- Pydantic
- UV (gerenciador de projeto)
- SQLite
- Docker
- BeautifulSoup

## Estrutura do Projeto

```
tc-ml-books/
├── src/
│   ├── api/           # Handlers das rotas FastAPI
│   ├── core/          # Utilitários, configuração, segurança
│   ├── crud/          # Lógica de acesso ao banco de dados
│   ├── data/          # Arquivos gerados pelo scrape
│   ├── middlewares/   # Logs e rate limit
│   ├── models/        # Modelos SQLAlchemy
│   ├── schemas/       # Schemas Pydantic
│   ├── scripts/       # Scripts para scraper e carga inicial da base
│   └── main.py        # Ponto de entrada da aplicação FastAPI
├── pyproject.toml
├── README.md
└── ...
```

## Primeiros Passos

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/tc-ml-books.git
cd tc-ml-books
```

### 2. Instale as dependências

#### O projeto utiliza o UV para gerenciamento de pacotes.
Instale seguindo sua a documentação, de acordo com o seu sistema operacional. [Documentação UV](https://docs.astral.sh/uv/getting-started/installation/)

#### Instalação das dependências utilizando comandos UV
```bash
uv venv
source .venv/bin/activate
uv pip install .
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```
DATABASE_URL=sqlite:///./nome-banco.db
SECRET_KEY=sua-chave-secreta
```

### 4. Execute as migrações do banco de dados

```bash
alembic upgrade head
```

### 5. Inicie a API

```bash
uvicorn src.main:app --reload
```

A API estará disponível em [http://localhost:8000](http://localhost:8000).

## Documentação da API

Documentação interativa disponível em:

- [Swagger UI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)

## Exemplos de Uso

### Listar todos os livros

```http
GET /api/books/
```

### Obter estatísticas dos livros

```http
GET /api/stats/overview
```

### Obter features de ML para um livro

```http
GET /api/ml/features/{book_id}
```

## Docker (opcional)

Construa e rode com Docker:

```bash
docker build -t tc-ml-books .
docker run -p 8000:8000 tc-ml-books
```

## Licença

MIT License

---

