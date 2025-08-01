import csv
from pathlib import Path
from src.models import Book, RatingEnum, Category
from src.core import get_db

def load_csv_to_db(db_session, csv_file_path: str):
    """    
    Load book data from a CSV file into the database.
    """
    try:
        categories_processed = set()
        categorias_db_map = {}

        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                category_name = row['Category'].strip()

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
    finally:
        db_session.close()

if __name__ == "__main__":
    db = get_db()
    SCRIPT_DIR = Path(__file__).resolve().parent
    PATH_FILE = SCRIPT_DIR.parent / 'data' / 'books_toscrape.csv'
    load_csv_to_db(db, PATH_FILE)