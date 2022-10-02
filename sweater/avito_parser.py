import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.avito.ru"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"


class NotFound(Exception):
    pass


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers={"user-agent": USER_AGENT})
    if response.status_code != 200:
        raise NotFound
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_products(url):
    try:
        soup = get_soup(url)
    except NotFound:
        return []
    products = soup.find_all("div", class_="iva-item-content-rejJg")
    products_dicts = []
    for product in products:
        product_dict = {
            "name": product.find("a", class_="link-link-MbQDP").text,
            "price": int(product.find("meta", itemprop="price").get("content")),
            "link": BASE_URL + product.find("a", class_="link-link-MbQDP").get("href"),
        }
        try:
            product_dict["seller_link"] = BASE_URL + product.find("a", class_="style-link-STE_U").get("href")
        except AttributeError:
            product_dict["seller_link"] = ""
        products_dicts.append(product_dict)
    return products_dicts


def get_product_price(url):
    try:
        soup = get_soup(url)
    except NotFound:
        return {}
    return {
        "price": int(soup.find("span", class_="js-item-price").get("content"))
    }


def get_sellers_products(seller_url):
    try:
        soup = get_soup(seller_url)
    except NotFound:
        return []
    products_dicts = []
    for product in soup.find_all("div", class_="ItemsShowcase-item-QXbIz"):
        products_dicts.append({
            "name": product.find("a", class_="link-link-MbQDP").text,
            "price": int(product.find("meta", itemprop="price").get("content")),
            "link": BASE_URL + product.find("a", class_="link-link-MbQDP").get("href"),
            "seller_link": seller_url
        })
    return products_dicts


if __name__ == '__main__':
    print(get_sellers_products("https://www.avito.ru/user/66261cb9a1b2d4469c0cfbc24347862b/profile?id=2540858771"))
