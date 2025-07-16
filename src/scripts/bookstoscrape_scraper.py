import os
from pathlib import Path
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
logging.info(f"Iniciando scraper para {books_toscrape_url}")

try:
    response = requests.get(books_toscrape_url)
    response.raise_for_status() 
    logging.info(f"Conexão bem-sucedida a url {books_toscrape_url} !")
except requests.exceptions.RequestException as e:
    logging.exception(f"Erro ao acessar a url {books_toscrape_url}: {e}")
    exit()
else:
    soup = BeautifulSoup(response.content, 'html.parser')
    start_time = time.perf_counter()

    categories = soup.find('ul', class_='nav-list').find_all('li')

    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)        
        path_target_file =  os.path.join(project_root, 'data', 'books_toscrape.csv')

        total_books = 0

        with open(path_target_file, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Category', 'Title', 'Price', 'Availability', 'Rating', 'Image URL'])

            for category in categories:
                category_name = category.a.text.strip()

                if category_name == 'Books':
                    continue
                
                category_url = books_toscrape_url + category.a['href']
                            
                response = requests.get(category_url)
                response.raise_for_status()
            
                soup = BeautifulSoup(response.content, 'html.parser')

                books = soup.find_all('article', class_='product_pod')
                total_books_category = len(books)
                total_books += total_books_category

                logging.info(f"Encontrados {total_books_category} livros na categoria {category_name}.")

                if not books:
                    logging.warning(f"Nenhum livro encontrado na categoria {category_name}.")
                else:                  
                    for book in books:
                        title = book.h3.a['title']
                        price = book.find('p', class_='price_color').text
                        availability = book.find('p', class_='instock availability').text.strip()
                        rating = book.p['class'][1]
                        image_url = books_toscrape_url + book.find('img')['src']

                        csv_writer.writerow([category_name, title, price, availability, rating, image_url])    
        logging.info(f"Dados salvos com sucesso em 'books_toscrape.csv'! Foram importados {total_books} livros.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao fazer a requisição HTTP: {e}")
    except IOError as e:
        logging.error(f"Erro ao escrever no arquivo CSV: {e}")
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado: {e}")

finally:
    end_time = time.perf_counter()
    logging.info(f"Tempo total de execução: {end_time - start_time:.2f} segundos")

