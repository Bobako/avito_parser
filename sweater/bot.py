import telebot
from telebot import types
from sweater.models import Query
from sweater import db
from sweater.avito_parser import query_products

bot = telebot.TeleBot("5604364570:AAGEDPpjj6doQriHWMJjCvUe4ULs2VDHwfg")


login_id = []


#def test():
#    with db.session() as session:
#        obj = session.query(Class).first()


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('/password')
    bot.send_message(message.chat.id, 'Введите пароль:',
                     reply_markup=keyboard)


@bot.message_handler(commands=['products'])
def start_message(message):
    if message.chat.id not in login_id:
        bot.send_message(message.chat.id, "Сначала введите пароль.")
        return

    bot.send_message(message.chat.id, "Вывод...")


@bot.message_handler(commands=['new'])
def new_product_query(message):
    if message.chat.id not in login_id:
        bot.send_message(message.chat.id, "Сначала введите пароль.")
        return
    send = bot.send_message(message.chat.id, "Введите наименование товара:")
    bot.register_next_step_handler(send, new_product)


def new_product(message):
    if message.text == 'Отмена':
        bot.send_message(message.chat.id, "Отмена, введите команду заново")
        return
    query_name = message.text
    query_obj = Query(query_name)
    with db.session() as session:
        session.add(query_obj)
        bot.send_message(message.chat.id, "Наименование внесено в базу данных.")


@bot.message_handler(content_types=['text'])
def start_message(message):
    if message.text.lower() == 'avito':
        login_id.append(message.chat.id)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row('/new', '/products', 'Отмена')
        bot.send_message(message.chat.id, 'Добро пожаловать!',
                         reply_markup=keyboard)
