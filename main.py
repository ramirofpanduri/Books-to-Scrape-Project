from scraper.database import get_db_connection
from scraper.categories import get_categories
from scraper.books import scrape_books_category

url = "http://books.toscrape.com/"


def main():
    conn = get_db_connection()
    cursor = conn.cursor()

    categories = get_categories(url)

    scrape_books_category(categories, cursor, conn)
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
