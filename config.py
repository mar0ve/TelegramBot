import logging
from aiogram import Bot, Dispatcher
from db import ManageDatabase
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = ''

db_connection = {
    "host": "localhost",
    "user": "root",
    "password": "12345",
    "database": "telegram_bot",
}

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db_manager = ManageDatabase(**db_connection)
