import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"

star_numbers = {
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
    print(f"Category: {name}")
    page_number = 1
