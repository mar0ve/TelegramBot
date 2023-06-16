import logging
from aiogram import Bot, Dispatcher, executor, types
import markup as nav
from config import TOKEN, db_connection
from db import ManageDatabase
from text import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db_manager = ManageDatabase(**db_connection)


@dp.message_handler(commands=['start',])
async def send_start(message: types.Message):
    chat_id = message.chat.id
    user = db_manager.check_user(chat_id)

    if user is None:
        await bot.send_message(chat_id,
                               '', reply_markup=nav.regMarkup)

    else:
        await bot.send_message(chat_id,
                               alreadyReg, reply_markup=nav.userMarkup)


@dp.message_handler()
async def bot_message(message: types.Message):
    #define user
    chat_id = message.chat.id
    user = db_manager.check_user(chat_id)

    match message.text:
        case regBtnText:
            if user is None:
                await bot.send_message(chat_id, regWelcome)
                full_name = message.text.split(' ')
                first_name = full_name[0]
                last_name = full_name[1] if len(full_name) > 1 else ''
                db_manager.register_user(chat_id, first_name, last_name)

                await bot.send_message(chat_id, applyReg)
            else:
                await bot.send_message(chat_id, alreadyReg)

        case

