import requests
from bs4 import BeautifulSoup


def get_categories(url):

    response = requests.get(url, timeout=20)

    soup = BeautifulSoup(response.text, "html.parser")

    category_list = soup.select("div.side_categories ul li ul li a")

    categories = []
    for cat in category_list:
        name = cat.text.strip()
        relative_link = cat["href"]
        full_link = url + relative_link
        categories.append((name, full_link))
