import os
from pathlib import Path
from urllib.parse import urljoin
import requests
import time
import csv
import logging
from bs4 import BeautifulSoup

# Configuração do logging
script_dir = Path(__file__).resolve().parent
log_file_path = script_dir / 'log_scraping.txt'
logging.basicConfig(
    level=logging.INFO,
    filename=log_file_path,
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

books_toscrape_url = 'http://books.toscrape.com/'

def scrape_book_data() -> str:
    """Scrape book data from Books to Scrape and save to CSV."""
    session = requests.Session()
    start_time = time.perf_counter()

    try:
        logging.info(f"Acessando a página inicial: {books_toscrape_url}")
        response = session.get(books_toscrape_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        logging.exception(f"Erro ao acessar a página inicial de {books_toscrape_url}: {e}")
        exit()
            
    # Define the path for the CSV file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)        
    path_target_file =  os.path.join(project_root, 'data', 'books_toscrape.csv')
    total_books_scraped = 0

    try:
        
        with open(path_target_file, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Category', 'Title', 'Price', 'Availability', 'Rating', 'Image URL'])

            category_links = soup.select('div.side_categories ul.nav-list ul li a')

            for category in category_links:
                category_name = category.get_text(strip=True)

                if category_name == 'Books':
                    continue
                
                category_url = urljoin(books_toscrape_url, category['href'])
                current_page_url = category_url
                logging.info(f"Acessando a categoria: {category_name}")
                while current_page_url:
                    try:
                        page_response = session.get(current_page_url)
                        page_response.raise_for_status()
                        page_soup = BeautifulSoup(page_response.content, 'html.parser')
                        
                        books_on_page = page_soup.find_all('article', class_='product_pod')
                        if not books_on_page:
                            logging.warning(f"Nenhum livro encontrado na página {current_page_url}")
                            break 

                        for book in books_on_page:
                            title = book.h3.a['title']
                            price = book.find('p', class_='price_color').text.strip()
                            availability = book.find('p', class_='instock availability').text.strip()
                            rating = book.p['class'][1]
                            image_relative_url = book.find('img')['src']
                            image_url = urljoin(books_toscrape_url, image_relative_url.replace('../', ''))

                            csv_writer.writerow([category_name, title, price, availability, rating, image_url])
                            total_books_scraped += 1

                        # Searches for the "next" button to navigate to the next page
                        next_page_element = page_soup.find('li', class_='next')
                        if next_page_element and next_page_element.a:
                            next_page_url = urljoin(category_url, next_page_element.a['href'])
                            logging.info(f"Navegando para a próxima página: {next_page_url}")
                            current_page_url = next_page_url
                        else:
                            current_page_url = None
                    except requests.exceptions.RequestException as e:
                        logging.error(f"Erro ao acessar a página {current_page_url}: {e}")
                        current_page_url = None 
  
        logging.info(f"Dados salvos com sucesso em 'books_toscrape.csv'! Foram importados {total_books_scraped} livros.")
        return path_target_file
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao fazer a requisição HTTP: {e}")
    except IOError as e:
        logging.error(f"Erro ao escrever no arquivo CSV: {e}")
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado: {e}")

    finally:
        end_time = time.perf_counter()
        logging.info(f"Tempo total de execução: {end_time - start_time:.2f} segundos")

if __name__ == "__main__":
    scrape_book_data()

