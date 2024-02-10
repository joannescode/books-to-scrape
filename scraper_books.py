import requests
from bs4 import BeautifulSoup


class ScraperBooks:
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

    def parser_product_urls(self):
        self.product_urls = [
            self.url_base + address["href"]
            for image_container in self.soup.find_all("div", class_="image_container")
            for address in image_container.find_all("a", href=True)
            if "catalogue" in address["href"]
            and "category" not in address["href"]
            and "page-" not in address["href"]
        ]

    def scrape_all_products(self):
        for url in self.product_urls:
            self.scrape_product_page(url)

    def scrape_product_page(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.find("h1").text.strip()
            price = soup.find("p", class_="price_color").text.strip()
            rows_table = soup.find_all("tr")
            aviability = rows_table[5].text.strip()
            paragraphs = soup.find_all("p")
            description = paragraphs[3].text.strip()

            print("Title:", title)
            print("Price:", price)
            print(aviability)
            print(f"\nDescription: {description} \n")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")


# Example usage:
scraper = ScraperBooks()
scraper.requests_page()
scraper.parser_product_urls()
scraper.scrape_all_products()
scraper.scrape_product_page()
