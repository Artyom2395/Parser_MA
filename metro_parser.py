import requests
import re
import csv
import lxml
from bs4 import BeautifulSoup

class MetroScraper:
    def __init__(self, city_id, city_name):
        self.city_id = city_id
        self.city_name = city_name
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.shema = "https://online.metro-cc.ru"
        self.base_url = f"https://online.metro-cc.ru/category/molochnye-prodkuty-syry-i-yayca/syry?from=under_search&page=1"

    def create_csv_file(self):
        filename = f"products_{self.city_name}.csv"
        self.csv_file = open(filename, "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.csv_file)
        self.writer.writerow(["id", "наименование", "ссылка", "регулярная цена, руб.", "промо цена, руб.", "бренд"])

    def scrape_data(self):
        flag = True
        while flag:
            cookies = {
                'metroStoreId': str(self.city_id),
            }
            response = requests.get(self.base_url, headers=self.headers, cookies=cookies)
            soup = BeautifulSoup(response.text, "lxml")
            divs = soup.select('div[data-sku]')
            pagination = soup.find("ul", class_="catalog-paginate")
            next_pages = self.shema + pagination.find_all("li")[-1].find("a").get("href")

            for div in divs:
                data_sku = div.get("data-sku")
                name = div.find("a", {"data-qa":"product-card-name"}).text.strip()
                product_url = self.shema + div.find("a", {"data-qa":"product-card-name"}).get("href")
                promo_price_el = div.find("span", class_=re.compile("product-price nowrap product-card-prices__actual"))
                if promo_price_el is None:
                    flag = False
                    break
                promo_price = promo_price_el.find(class_=re.compile("product-price__sum-rubles")).text
                reg_price = div.find("span", class_=re.compile("product-price nowrap product-card-prices__old"))

                if reg_price is None:
                    reg_price = promo_price
                    promo_price = "нет скидки"
                else:
                    reg_price = reg_price.find(class_=re.compile("product-price__sum-rubles")).text

                response = requests.get(product_url)
                soup = BeautifulSoup(response.text, "lxml")
                brand_element = soup.find_all("li", class_="product-attributes__list-item")[0]
                span_element = brand_element.find("span", class_="product-attributes__list-item-dots")
                next_element = span_element.find_next()
               
                if next_element.name == "a" or next_element.name == "span":
                    brand = next_element.text.strip()
                else:
                    brand = None
               
                self.writer.writerow([data_sku, name, product_url, reg_price, promo_price, brand])
               
            if next_pages != self.base_url:
                self.base_url = next_pages
            else:
                flag = False

        print(f"Data scraped for {self.city_name}.csv")
        self.csv_file.close()

## Использование класса
#moscow_scraper = MetroScraper(10, "Moscow")
#moscow_scraper.create_csv_file()
#moscow_scraper.scrape_data()

spb_scraper = MetroScraper(15, "Saint Petersburg")
spb_scraper.create_csv_file()
spb_scraper.scrape_data()
