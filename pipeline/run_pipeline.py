import sys
import structlog
from src.scripts.bookstoscrape_scraper import scrape_book_data
from src.scripts.seed import load_csv_to_db
from src.core.database import get_db

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)
log = structlog.get_logger()

def main():
    """
    Main function that orchestrates the scraping and loading pipeline.
    """
    log.info("Data pipeline started.")
    
    # Create a database session to be used by the pipeline
    db = get_db()
    
    try:
        log.info("Starting scraping step...")

        csv_path = scrape_book_data()
        log.info(f"Scraping finished. Data saved at: {csv_path}")

        log.info("Starting loading step to the database...")        
        load_csv_to_db(db=db, csv_file_path=csv_path)
        log.info("Data loading completed successfully.")

        log.info("Data pipeline completed successfully!")

    except Exception as e:
        log.error(f"A fatal error occurred in the pipeline: {e}", exc_info=True)
        sys.exit(1)
        
    finally:
        db.close()
        log.info("Database connection closed.")

if __name__ == "__main__":
    main()