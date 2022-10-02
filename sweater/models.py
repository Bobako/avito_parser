import datetime
import logging
from contextlib import contextmanager

import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session, backref

Base = declarative_base()


class Database:
    """
    Класс для подключения к базе данных и использования потокобезопасной сессии работы с ней.
    """

    def __init__(self, database_url: str):
        """
        Args:
            database_url: адрес базы данных, например postgresql+psycopg2://postgres:postgrespw@localhost:55000
        """
        engine = sqlalchemy.create_engine(database_url)
        Base.metadata.create_all(engine)
        self.sessionmaker = sessionmaker(bind=engine)
        logging.info("База данных подключена")

    @contextmanager
    def session(self):
        """
        Фабричная функция для scoped (т.е. thread-local и thread-safe) session,
        поддерживающая инструкцию with.
        """
        exception = None
        session = scoped_session(self.sessionmaker)
        try:
            yield session
        except Exception as ex:
            logging.error(ex)
            session.rollback()
            exception = ex
        else:
            session.commit()
        finally:
            session.close()
        if exception:
            raise exception


class Product(Base):
    __tablename__ = "product"
    url = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    seller_link = Column(String)
    query_name = Column(String)
    last_update = Column(DateTime)

    def __init__(self, url, name, price, query_name, seller_link):
        self.url = url
        self.name = name
        self.price = price
        self.query_name = query_name
        self.last_update = datetime.datetime.now()
        self.seller_link = seller_link

    def update(self, price):
        self.price = price
        self.last_update = datetime.datetime.now()

    def __repr__(self):
        return f"{self.name} - {self.price}:{self.url}"


class Query(Base):
    __tablename__ = "query"
    name = Column(String, primary_key=True)

    def __init__(self, query_name):
        self.name = query_name
