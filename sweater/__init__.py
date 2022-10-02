from threading import Thread

from sweater.models import Database

db_url = "sqlite:///database.db"
db = Database(db_url)

from sweater.bot import bot
from sweater.avito_parser import run as run_parser


def main():
    t1 = Thread(target=bot.infinity_polling)
    t2 = Thread(target=run_parser)
    t1.start()
    t2.start()
