import requests
import time
from bs4 import BeautifulSoup

books_toscrape_url = 'http://books.toscrape.com/'

print(f"Iniciando scraper para {books_toscrape_url}")

try:
    response = requests.get(books_toscrape_url)
    response.raise_for_status() 
    print("Conexão bem-sucedida!")
except requests.exceptions.RequestException as e:
    print(f"Erro ao acessar a url {books_toscrape_url}: {e}")
    exit()
else:
    soup = BeautifulSoup(response.content, 'html.parser')
    start_time = time.perf_counter()

    categories = soup.find('ul', class_='nav-list').find_all('li')

    for category in categories:
        category_name = category.a.text.strip()
        category_url = books_toscrape_url + category.a['href']

        print(f"Buscando livros na categoria: {category_name}")

        try:
            response = requests.get(category_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a página {category_url}: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        books = soup.find_all('article', class_='product_pod')

        if not books:
            print("Nenhum livro encontrado.")
        else:
            print(f"Total de livros encontrados: {len(books)}")
            for book in books:
                title = book.h3.a['title']
                price = book.find('p', class_='price_color').text
                availability = book.find('p', class_='instock availability').text.strip()
                print(f"Título: {title}, Preço: {price}, Disponibilidade: {availability}")

        #counter_page = soup.find('li', class_='current').text.strip()
        #qtd_pages = counter_page.split()[-1]
        #current_page = counter_page.split()[1]
     
        end_time = time.perf_counter()
finally:
    print(f"Tempo total de execução: {end_time - start_time:.2f} segundos")

