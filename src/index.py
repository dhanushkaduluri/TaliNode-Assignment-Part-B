import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Function to scrape books data from the website
def scrape_books_data():
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    books_data = []

    for page_num in range(1, 51):  # Scrape data from 50 pages
        url = base_url.format(page_num)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        books = soup.find_all('article', class_='product_pod')
        for book in books:
            title = book.h3.a['title']
            price_str = book.find('p', class_='price_color').text
            price = float(''.join(filter(str.isdigit, price_str))) / 100  # Extract digits and convert to float
            availability = book.find('p', class_='instock availability').text.strip()
            rating = book.find('p', class_='star-rating')['class'][1]
            books_data.append({"title": title, "price": price, "availability": availability, "rating": rating})

    return books_data


# Function to store books data in MongoDB
def store_books_data_in_mongodb(books_data):
    client = MongoClient('localhost', 27017)
    db = client['books_db']
    books_collection = db['books']

    # Clear existing data
    books_collection.delete_many({})

    # Insert new data
    books_collection.insert_many(books_data)

    client.close()

def main():
    books_data = scrape_books_data()
    store_books_data_in_mongodb(books_data)
    print("Books data scraped and stored successfully.")

if __name__ == "__main__":
    main()

