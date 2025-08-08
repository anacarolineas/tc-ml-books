import csv
import logging

from pathlib import Path
from src.models.book import Book, RatingEnum
from src.models.category import Category
from src.core.database import get_db

script_dir = Path(__file__).resolve().parent
log_file_path = script_dir / 'log_seed.txt'
logging.basicConfig(
    level=logging.INFO,
    filename=log_file_path,
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_csv_to_db(db_session, csv_file_path: str):
    """    
    Load book data from a CSV file into the database.
    """
    try:
        logging.info("Iniciando carga da base de dados....")
        logging.info("Limpando a base de dados...")
        
        db_session.query(Book).delete()
        db_session.query(Category).delete()

        categories_processed = set()
        categorias_db_map = {}

        logging.info(f"Iniciando leitura do csv.")
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                category_name = row['Category'].strip()
                logging.info(f"Inserindo livro da categoria: {category_name} - {row['Title'].strip()}")
                if category_name not in categories_processed:
                    new_category = Category(name=category_name)
                    db_session.add(new_category)
                    
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
                db_session.add(book)

            db_session.commit()
    except Exception as e:
        db_session.rollback()
        logging.info(f"Erro inesperado: {e}")
    finally:
        logging.info("Carga da base finalizada.")
        db_session.close()

if __name__ == "__main__":
    db_session = next(get_db())
    SCRIPT_DIR = Path(__file__).resolve().parent
    PATH_FILE = SCRIPT_DIR.parent / 'data' / 'books_toscrape.csv'
    load_csv_to_db(db_session, PATH_FILE)