import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def web_scraping_books(save_path, url=None):
    # Set default URL if none provided
    target_url = url if url else "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    
    # Configure headers for the request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # First try with default settings
        response = requests.get(target_url, verify=False, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.RequestException:
        try:
            # If first attempt fails, try with additional headers
            headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            })
            response = requests.get(target_url, verify=False, headers=headers, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch the URL: {str(e)}")
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    books = []
    
    # Check if this is the books.toscrape.com site
    if 'books.toscrape.com' in target_url:
        for book in soup.find_all('article', class_='product_pod'):
            title = book.h3.a.get('title', 'N/A')
            price = book.find('p', class_='price_color').text if book.find('p', class_='price_color') else 'N/A'
            rating = book.p['class'][1] if book.p and 'class' in book.p.attrs and len(book.p['class']) > 1 else 'N/A'
            books.append([title, price, rating])
        
        df = pd.DataFrame(books, columns=["Title", "Price", "Rating"])
    else:
        # Generic scraping for other websites - this is a basic example
        for item in soup.find_all(['article', 'div'], class_=True):  # Look for articles or divs with classes
            title = item.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'span'])
            price = item.find(class_=lambda x: x and ('price' in x.lower() or 'cost' in x.lower()))
            
            if title:
                title = title.get_text(strip=True)
                price = price.get_text(strip=True) if price else 'N/A'
                books.append([title, price, 'N/A'])
        
        df = pd.DataFrame(books, columns=["Title", "Price", "Details"]) if books else pd.DataFrame(columns=["Message"], data=[["No data could be extracted. The website might have a different structure."]])
    df.to_csv(save_path, index=False)
    return df
