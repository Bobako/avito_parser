from sweater.models import Database

db_url = "sqlite:///database.db"
db = Database(db_url)

from sweater.bot import bot
from sweater.avito_parser import run as run_parser

def main():
    bot.infinity_polling()
