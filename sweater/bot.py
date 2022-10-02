import telebot
from telebot import types

from sweater import db

bot = telebot.TeleBot("5604364570:AAGEDPpjj6doQriHWMJjCvUe4ULs2VDHwfg")

# conn = psycopg2.connect(database="avito_db",
#                        user="postgres",
#                        password="123",
#                        host="localhost",
#                        port="5432")

# cursor = conn.cursor()


login_id = []


#def test():
#    with db.session() as session:
#        obj = session.query(Class).first()


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('/password')
    bot.send_message(message.chat.id, 'Введите пароль',
                     reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def start_message(message):
    if message.text.lower() == 'avito':
        login_id.append(message.chat.id)


@bot.message_handler(commands=['products'])
def start_message(message):
    if message.chat.id not in login_id:
        bot.send_message(message.chat.id, "Сначала введите пароль.")
        return
    bot.send_message(message.chat.id, "Вывод...")


bot.infinity_polling()
