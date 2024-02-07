import requests
from bs4 import BeautifulSoup


class ScrapeBooks:
    def __init__(self) -> None:
        self.url_base = "https://books.toscrape.com/"
        self.thumbnail_addresses = []

    def requests_page(self):
        try:
            response = requests.get(f"{self.url_base}index.html")
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def parser_thumbnail_address(self):
        self.thumbnail_addresses = [
            address["href"]
            for image_container in self.soup.find_all("div", class_="image_container")
            for address in image_container.find_all("a", href=True)
            if "catalogue" in address["href"]
            and "category" not in address["href"]
            and "page-" not in address["href"]
        ]

    def get_thumbnail_address(self):
        for url_thumbnail in self.thumbnail_addresses:
            try:
                response_catalogue = requests.get(f"{self.url_base}{url_thumbnail}")
                response_catalogue.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url_thumbnail}: {e}")

    def parser_title_book(self):
        for url_thumbnail in self.thumbnail_addresses:
            try:
                response_catalogue = requests.get(f"{self.url_base}{url_thumbnail}")
                response_catalogue.raise_for_status()
                soup_book = BeautifulSoup(response_catalogue.text, "html.parser")
                for informations in soup_book.find_all(
                    "div", class_="col-sm-6 product_main"
                ):
                    for title_book in informations.find_all("h1"):
                        print(title_book.text)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url_thumbnail}: {e}")
                
    def parser_price_book(self):
        for url_thumbnail in self.thumbnail_addresses:
            try:
                response_catalogue = requests.get(f"{self.url_base}{url_thumbnail}")
                response_catalogue.raise_for_status()
                soup_book = BeautifulSoup(response_catalogue.text, "html.parser")
                for informations in soup_book.find_all(
                    "table", class_="table table-striped"
                ):
                    for price_book in informations.find_all("td")[3]:
                        print(price_book.text)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url_thumbnail}: {e}")

                
# Example usage:
scraper = ScrapeBooks()
scraper.requests_page()
scraper.parser_thumbnail_address()
scraper.get_thumbnail_address()
scraper.parser_title_book()
scraper.parser_price_book()
