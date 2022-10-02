from sweater.models import Database

db_url = "sqlite:///database.db"
db = Database(db_url)

from sweater.bot import bot


def main():
    bot.infinity_polling()
