import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import time
import mysql.connector

load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
cursor = conn.cursor()

url = "https://books.toscrape.com/"

star_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

response = requests.get(url, timeout=20)
soup = BeautifulSoup(response.text, "html.parser")

full_article = soup.select("article.product_pod")
category_list = soup.select("div.side_categories ul li ul li a")

categories = []
for cat in category_list:
    name = cat.text.strip()
    relative_link = cat["href"]
    full_link = url + relative_link
    categories.append((name, full_link))

category_id_map = {}

for name, link in categories:
    cursor.execute("INSERT IGNORE INTO categories (name) VALUES (%s)", (name,))
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
            page_url = link.replace("index.html", f"page-{page_number}.html")

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

            category_id = category_id_map[name]

            print(f"  - {title} | {price} | Stars: {stars}")

            cursor.execute(
                "INSERT IGNORE INTO books (title, price, stars, category_id) VALUES (%s, %s, %s, %s)",
                (title, price, stars, category_id)
            )
            conn.commit()

        page_number += 1

cursor.close()
conn.close()
