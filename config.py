import logging
from aiogram import Bot, Dispatcher, executor, types
from db import ManageDatabase
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from text import applyReg
from markup import userMarkup

TOKEN = '6257891124:AAEmx-mDLRp_jjG7EeAVOpOkHdtWHonFhHg'

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