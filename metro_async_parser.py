import aiohttp
import asyncio
import csv
import re
from bs4 import BeautifulSoup

async def create_csv_file(city):
    filename = f"products_{city}.csv"
    csv_file = open(filename, "w", newline="", encoding="utf-8")
    writer = csv.writer(csv_file)

    writer.writerow(["id", "наименование", "ссылка", "регулярная цена, руб.", "промо цена, руб.", "бренд"])

    return csv_file, writer

async def make_request(session, url, headers, cookies):
    async with session.get(url, headers=headers, cookies=cookies) as response:
        return await response.text()

async def scrape_data_for_city(city_id, city_name, writer):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    url = f"https://online.metro-cc.ru/category/molochnye-prodkuty-syry-i-yayca/syry?from=under_search&page=1"
    flag = True

    async with aiohttp.ClientSession() as session:
        while flag:
            cookies = {
                'metroStoreId': str(city_id),
            }

            html = await make_request(session, url, headers, cookies)
            soup = BeautifulSoup(html, "lxml")
            shema = "https://online.metro-cc.ru"

            divs = soup.select('div[data-sku]')
            pagination = soup.find("ul", class_="catalog-paginate")
            next_pages = shema + pagination.find_all("li")[-1].find("a").get("href")

            # Обходим каждый найденный div
            for div in divs:
                # Получаем значение атрибута data-sku
                data_sku = div.get("data-sku")
                name = div.find("a", {"data-qa":"product-card-name"}).text.strip()
                product_url = shema + div.find("a", {"data-qa":"product-card-name"}).get("href")
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

                product_html = await make_request(session, product_url, headers, {})
                product_soup = BeautifulSoup(product_html, "lxml")
                brand_element = product_soup.find_all("li", class_="product-attributes__list-item")[0]
                span_element = brand_element.find("span", class_="product-attributes__list-item-dots")
                next_element = span_element.find_next()

                if next_element.name == "a" or next_element.name == "span":
                    brand = next_element.text.strip()
                else:
                    brand = None

                writer.writerow([data_sku, name, product_url, reg_price, promo_price, brand])

            if next_pages != url:
                url = next_pages
            else:
                flag = False

    print(f"Data scraped for {city_name}.csv")


# Использование функций

async def main():
    # Создание файла для Москвы
    moscow_csv_file, moscow_writer = await create_csv_file("moscow")
    await scrape_data_for_city(10, "Moscow", moscow_writer)
    moscow_csv_file.close()

    # Создание файла для Санкт-Петербурга
    #spb_csv_file, spb_writer = await create_csv_file("saint_petersburg")
    #await scrape_data_for_city(15, "Saint Petersburg", spb_writer)
    #spb_csv_file.close()

# Запуск асинхронной функции
loop = asyncio.get_event_loop()
loop.run_until_complete(main())