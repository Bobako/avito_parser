#import psycopg2

import datetime
import telebot
from telebot import types


bot = telebot.TeleBot("5604364570:AAGEDPpjj6doQriHWMJjCvUe4ULs2VDHwfg")

#conn = psycopg2.connect(database="avito_db",
#                        user="postgres",
#                        password="123",
#                        host="localhost",
#                        port="5432")

#cursor = conn.cursor()


login_id = []



def password(message):
    login = False
    if message.text.lower() == 'avito':
        login = True
    bot.send_message(message.chat.id, 'Здравствуйте!')
    return login


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('/password')
    bot.send_message(message.chat.id, 'Введите пароль',
                     reply_markup=keyboard)



@bot.message_handler(content_types=['text'])
def start_message(message):
    nom = -1
    if message.text.lower() == 'avito':
        login_id.append(message.chat.id)
    if message.chat.id in login_id:
        password()



bot.infinity_polling()