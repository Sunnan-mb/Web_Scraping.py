import pandas as pd
import requests
from bs4 import BeautifulSoup


def web_scraping_books(save_path):
    url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = []
    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        rating = book.p['class'][1]
        books.append([title, price, rating])

    # Write data to an Excel file

    df = pd.DataFrame(books, columns=["Title", "Price", "Rating"])
    df.to_csv(save_path, index=False)
    return df
