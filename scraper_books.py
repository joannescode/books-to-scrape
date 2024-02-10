import requests
from bs4 import BeautifulSoup


class ScraperBooks:
    def __init__(self) -> None:
        self.url_base = "https://books.toscrape.com"
        self.product_urls = []
        self.thumbnail_addresses = []

    def requests_page(self, url):
        try:
            response = requests.get(self.url_base + url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def parser_product_urls(self):
        try:
            image_containers = self.soup.find_all("div", class_="image_container")
            for image_container in image_containers:
                link = image_container.find("a", href=True)
                if link:
                    product_url = link["href"]
                    if product_url.endswith("index.html"):
                        product_url = product_url[:-10]
                    if "catalogue" not in product_url:
                        product_url = self.url_base + "/catalogue/" + product_url
                    self.product_urls.append(product_url)
            print("Product URLs:", self.product_urls)
        except Exception as e:
            print("Error parsing product URLs:", e)

    def scrape_product_page(self):
        for url in self.product_urls:
            try:
                print("Scraping URL:", url)
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                title = soup.find("h1").text.strip()
                price = soup.find("p", class_="price_color").text.strip()
                rows_table = soup.find_all("tr")
                availability = rows_table[5].text.strip()
                paragraphs = soup.find_all("p")
                description = paragraphs[3].text.strip()

                print("Title:", title)
                print("Price:", price)
                print("Availability:", availability)
                print(f"\nDescription: {description} \n")

            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url}: {e}")


# Example usage:
scraper = ScraperBooks()
for number_page in range(1, 51):
    scraper.requests_page(url=f"/catalogue/page-{number_page}.html")
    scraper.parser_product_urls()

scraper.scrape_product_page()
