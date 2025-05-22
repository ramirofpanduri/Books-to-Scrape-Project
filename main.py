import requests
from bs4 import BeautifulSoup
import time

url = "https://books.toscrape.com/"

star_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

full_article = soup.select("article.product_pod")
category_list = soup.select("div.side_categories ul li ul li a")

categories = []
for cat in category_list:
    name = cat.text.strip()
    relative_link = cat["href"]
    full_link = url + relative_link
    categories.append((name, full_link))


for name, link in categories:
    print(f"\n Category: {name}")
    page_number = 1

    while True:
        if page_number == 1:
            page_url = link
        else:
            page_url = link.replace("index.html", f"page-{page_number}.html")

        res = requests.get(page_url)
        time.sleep(1)
        if res.status_code != 200:
            break

        page_soup = BeautifulSoup(res.text, "html.parser")
        books = page_soup.select("article.product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.select_one("p.price_color").text

            star_tag = book.select_one("p.star-rating")
            star_classes = star_tag.get("class", [])
            star_text = [c for c in star_classes if c != "star-rating"][0]
            stars = star_map.get(star_text, 0)

            print(f"  - {title} | {price} | Estrellas: {stars}")

        page_number += 1
