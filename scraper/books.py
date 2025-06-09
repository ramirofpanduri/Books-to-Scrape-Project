import time
import requests
from bs4 import BeautifulSoup
from scraper.utils import star_map


def scrape_books_category(categories, cursor, conn):
    category_id_map = {}

    for name, link in categories:

        cursor.execute(
            "INSERT IGNORE INTO categories (name) VALUES (%s)", (name,))
        conn.commit()

        cursor.execute("SELECT id FROM categories WHERE name = %s", (name,))
        category_id = cursor.fetchone()[0]
        category_id_map[name] = category_id

        print(f"\n Category: {name} (ID: {category_id})")

        page_number = 1

        while True:
            if page_number == 1:
                page_url = link
            else:
                page_url = link.replace(
                    "index.html", f"page-{page_number}.html")

            res = requests.get(page_url, timeout=20)
            time.sleep(1)
            if res.status_code != 200:
                break

            page_soup = BeautifulSoup(res.text, "html.parser")
            books = page_soup.select("article.product_pod")

            for book in books:
                title = book.h3.a["title"]
                price_text = book.select_one("p.price_color").text.strip()
                price = float(price_text.replace("£", "").replace("Â", ""))

                star_tag = book.select_one("p.star-rating")
                star_classes = star_tag.get("class", [])
                star_text = [c for c in star_classes if c != "star-rating"][0]
                stars = star_map.get(star_text, 0)

                print(f"  - {title} | {price} | Stars: {stars}")

                cursor.execute(
                    "INSERT IGNORE INTO books (title, price, stars, category_id) VALUES (%s, %s, %s, %s)",
                    (title, price, stars, category_id)
                )
                conn.commit()

            page_number += 1
