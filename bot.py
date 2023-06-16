import telebot
from telebot import types
import mysql.connector
from tabulate import tabulate
from db import ManageDatabase
from config import db_connection, TOKEN
from text import *


bot = telebot.TeleBot(TOKEN)
db_manager = ManageDatabase(**db_connection)


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    user = db_manager.check_user(chat_id)

    if user is None:
        bot.reply_to(message, regWelcome)
    else:
        bot.reply_to(message, alreadyReg)
        show_commands_keyboard(chat_id)


def generate_report(work_logs):
    table_data = []
    for log in work_logs:
        first_name, last_name, start_time, end_time = log
        end_time = end_time if end_time is not None else "В процессе"
        table_data.append([first_name, last_name, start_time, end_time])

    headers = ["Имя", "Фамилия", "Начало дня", "Конец дня"]
    report = tabulate(table_data, headers, tablefmt="fancy_grid")
    return report


def show_commands_keyboard(chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    keyboard.add(telebot.types.KeyboardButton("Начать рабочий день"))
    keyboard.add(telebot.types.KeyboardButton("Закончить рабочий день"))
    keyboard.add(telebot.types.KeyboardButton("Отчет"))
    keyboard.add(telebot.types.KeyboardButton("Отчет на всех"))

    bot.send_message(chat_id, "Выберите команду:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def handle_text(message):

    chat_id = message.chat.id
    user = db_manager.check_user(chat_id)

    if user is None:

        full_name = message.text.split(" ")
        first_name = full_name[0]
        last_name = full_name[1] if len(full_name) > 1 else ""
        db_manager.register_user(chat_id, first_name, last_name)

        bot.reply_to(message, applyReg)
    else:
        if message.text.lower() == "начать рабочий день":
            db_manager.start_workday(user[0])
            bot.reply_to(message, "рабочий день начат")

        elif message.text.lower() == "закончить рабочий день":
            db_manager.end_workday(user[0])
            bot.reply_to(message, "Рабочий день закончен")

        elif message.text.lower() == "отчет":
            # Выполнение запроса для получения отчета
            work_logs = db_manager.print_info(chat_id)
            # Формирование текстового отчета
            report = "Отчет о пребывании на работе:\n\n"
            for log in work_logs:
                first_name = log[0]
                last_name = log[1]
                start_time = log[2]
                end_time = log[3] if log[3] is not None else "В процессе"
                report += f"Имя: {first_name}\nФамилия: {last_name}\nНачало дня: {start_time}\nКонец дня: {end_time}\n\n"

            # Отправка текстового отчета пользователю
            bot.reply_to(message, report)

        elif message.text.lower() == 'отчет на всех':
            # Выполнение запроса для получения отчета
            work_logs = db_manager.print_all_info()

            # Формирование текстового отчета
            report = "Отчет о пребывании на работе:\n\n"
            for log in work_logs:
                first_name = log[0]
                last_name = log[1]
                start_time = log[2]
                end_time = log[3] if log[3] is not None else "В процессе"
                report += f"Имя: {first_name}\nФамилия: {last_name}\nНачало дня: {start_time}\nКонец дня: {end_time}\n\n"

            # Отправка текстового отчета пользователю
            bot.reply_to(message, report)

        show_commands_keyboard(chat_id)


bot.polling()



'''
pythonanywhere.com
user: mar0ve
pass: ?
email: marveevram@yandex.ru

db:
user = mar0ve
host = mar0ve.mysql.pythonanywhere-services.com
password = fucku1234
database = mar0ve$users_db
token = '6257891124:AAEmx-mDLRp_jjG7EeAVOpOkHdtWHonFhHg'
'''
