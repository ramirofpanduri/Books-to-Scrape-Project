# Books to Scrape - Web Scraper + Automation

This project collects book data from [books.toscrape.com](https://books.toscrape.com/) and saves it to a MySQL database. The scraper runs automatically every 24 hours using APScheduler.

---

## Technologies Used

- Python
- BeautifulSoup (web scraping)
- requests (HTTP)
- MySQL (database)
- APScheduler (scheduling)
- python-dotenv (for environment variables)

 ## Installation

It is necessary to create a virtual environment for the scraper to work. Pipenv was used, so it is highly recommended.

```bash
# Clone the repository
git clone https://github.com/ramirofpanduri/Scraper-Project-HF.git
cd Scraper-Project-HF

# Install dependencies using Pipenv
pipenv install

# Activate the virtual environment
pipenv shell
