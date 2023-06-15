import telebot
from telebot import types
import mysql.connector
from DBManager import ManageDatabase
from config import db_connection, TOKEN
# Подключение к базе данных MySQL


# Инициализация телеграм-бота
bot = telebot.TeleBot(TOKEN)
db_manager = ManageDatabase(**db_connection)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Получение идентификатора пользователя из сообщения
    chat_id = message.chat.id

    # Проверка, зарегистрирован ли пользователь в базе данных
    user = db_manager.check_user(chat_id)

    if user is None:
        # Если пользователь не зарегистрирован, запрашиваем его данные
        bot.reply_to(message, "Для регистрации введите ваше имя и фамилию в формате:\n\nИмя Фамилия")
    else:
        # Если пользователь уже зарегистрирован, отправляем ему сообщение
        bot.reply_to(message, "Вы уже зарегистрированы")

        # Отправляем всплывающее окно с командами
        show_commands_keyboard(chat_id)


# Функция для отображения всплывающего окна с командами
def show_commands_keyboard(chat_id):
    # Создание клавиатуры с кнопками
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    keyboard.add(telebot.types.KeyboardButton("Начать рабочий день"))
    keyboard.add(telebot.types.KeyboardButton("Закончить рабочий день"))
    keyboard.add(telebot.types.KeyboardButton("Отчет"))
    keyboard.add(telebot.types.KeyboardButton("Отчет на всех"))

    # Отправка всплывающего окна с командами пользователю
    bot.send_message(chat_id, "Выберите команду:", reply_markup=keyboard)


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    # Получение идентификатора пользователя из сообщения
    chat_id = message.chat.id

    # Проверка, зарегистрирован ли пользователь в базе данных
    user = db_manager.check_user(chat_id)

    if user is None:
        # Если пользователь не зарегистрирован, сохраняем его данные
        full_name = message.text.split(" ")
        first_name = full_name[0]
        last_name = full_name[1] if len(full_name) > 1 else ""
        db_manager.register_user(chat_id, first_name, last_name)

        bot.reply_to(message, "Вы успешно зарегистрированы")
    else:
        # Если пользователь уже зарегистрирован, выполняем действия по началу или окончанию рабочего дня
        if message.text.lower() == "начать рабочий день":
            # Записываем начало рабочего дня в базу данных
            db_manager.start_workday(user[0])
            bot.reply_to(message, "рабочий день начат")
        elif message.text.lower() == "закончить рабочий день":
            # Записываем окончание рабочего дня в базу данных
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





# Запуск телеграм-бота
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
