import requests
from bs4 import BeautifulSoup


class ScrapeBooks:
    def __init__(self) -> None:
        self.url_base = "https://books.toscrape.com/"
        self.thumbnail_addresses = []

    def requests_page(self):
        try:
            response = requests.get(f"{self.url_base}index.html")
            response.raise_for_status()  # Raise an HTTPError for bad responses
            self.soup = BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
