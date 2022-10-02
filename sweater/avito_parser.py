import datetime
import difflib
import logging
import time

import requests
import sqlalchemy
import sqlalchemy.exc
from bs4 import BeautifulSoup

from sweater import db
from sweater.models import Product, Query

BASE_URL = "https://www.avito.ru"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"


class NotFound(Exception):
    pass


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers={"user-agent": USER_AGENT})
    if response.status_code != 200:
        print(response.status_code)
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
    for i, product in enumerate(products):
        if i == 5:
            break
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


def query_products(query_name):
    """Get models.Product objs from query results"""
    url = "https://www.avito.ru/moskva?metro=9-131&q=" + query_name.replace(" ", "+")
    product_dicts = get_products(url)
    products_objs = []
    for product_dict in product_dicts:
        products_objs.append(Product(**product_dict, query_name=query_name))
    return products_objs


def is_similar(str1, str2):
    normalized1 = str1.lower()
    normalized2 = str2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio() >= 0.8


def update_all():
    with db.session() as session:
        products = session.query(Product).all()
        for product in products:
            product.update(**get_product_price(product.url))
            time.sleep(10)


def query_old():
    parsed = False
    with db.session() as session:
        queries = session.query(Query).filter(sqlalchemy.or_(
            Query.last_update <= datetime.datetime.now() - datetime.timedelta(3600 * 2),
            Query.last_update == None
        )).all()
        for query in queries:
            parsed = True
            print("пошли запросы по " + query.name)
            products = query_products(query.name)
            print(products)
            for product in products:
                try:
                    session.add(product)
                    session.commit()
                except sqlalchemy.exc.IntegrityError:
                    session.rollback()
            query.last_update = datetime.datetime.now()
    return parsed


def run():
    print('парсер крутится')
    while True:
        if not query_old():
            time.sleep(60)
        if datetime.datetime.now().hour % 6 == 0 and datetime.datetime.now().minute == 0:
            update_all()


if __name__ == '__main__':
    print(get_sellers_products("https://www.avito.ru/user/66261cb9a1b2d4469c0cfbc24347862b/profile?id=2540858771"))
