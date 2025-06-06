import time
import requests
from bs4 import BeautifulSoup
from utils import star_map


def scrape_books(name, link, category_id, cursor):
    page_number = 1
