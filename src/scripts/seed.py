import csv
import os
from pathlib import Path

from database import SessionLocal, engine
from models import Base, Book, Category, RatingEnum

Base.metadata.create_all(bind=engine)

session = SessionLocal()

try:
    print("Iniciando a carga de dados do arquivo CSV...")

    categories_processed = set()
    categorias_db_map = {}

    SCRIPT_DIR = Path(__file__).resolve().parent
    PATH_FILE = SCRIPT_DIR.parent / 'data' / 'books_toscrape.csv'
    print(f"Script directory: {PATH_FILE}")
    with open(PATH_FILE, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            category_name = row['Category'].strip()

            if category_name not in categories_processed:
                new_category = Category(name=category_name)
                session.add(new_category)
                
                categories_processed.add(category_name)
                categorias_db_map[category_name] = new_category

            current_category = categorias_db_map[category_name]

            book = Book(
                title=row['Title'].strip(),
                price=row['Price'].replace('£', '').strip(),
                availability='In stock' in row['Availability'].strip(),
                rating=RatingEnum[row['Rating'].strip()],
                image_url=row['Image URL'].strip(),
                category=current_category
            )
            session.add(book)

        session.commit()
        print("Carga de dados concluída com sucesso!")
except Exception as e:
    print(f"Ocorreu um erro durante a carga de dados: {e}")
    session.rollback()
finally:
    session.close()