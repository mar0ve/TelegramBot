from config import db_manager, dp, bot
from text import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from markup import userMarkup, adminMarkup, edtProfileMarkup, departmentsMarkup
from datetime import datetime


class AwaitMessages(StatesGroup):
    fio_add = State()
    phone_add = State()
    email_add = State()
    tel_link_add = State()
    department_add = State()


@dp.message_handler(state=AwaitMessages.fio_add)
async def process_fio_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fio'] = message.text

    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Введите телефон: ')
    await AwaitMessages.phone_add.set()


@dp.message_handler(state=AwaitMessages.phone_add)
async def process_phone_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Введите email: ')
    await AwaitMessages.email_add.set()


@dp.message_handler(state=AwaitMessages.email_add)
async def process_email_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text

    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Выберите отдел: ', reply_markup=departmentsMarkup)
    await AwaitMessages.department_add.set()


@dp.message_handler(state=AwaitMessages.department_add)
async def process_dep_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['department'] = message.text

    chat_id = message.chat.id
    full_name = data['fio'].split(' ')
    first_name = full_name[0]
    last_name = full_name[1]
    phone = data['phone']
    email = data['email']
    department = data['department']
    db_manager.register_user(chat_id, first_name, last_name, email, phone, datetime.now(), 'user', department)
    await state.finish()
    user_state = db_manager.is_admin(chat_id)
    markup = userMarkup if not user_state else adminMarkup
    await bot.send_message(chat_id, applyReg, reply_markup=userMarkup)


class SetUserData(StatesGroup):
    fio_set = State()
    email_set = State()
    phone_set = State()


@dp.message_handler(state=SetUserData.fio_set)
async def process_set_fio(message: types.Message, state: FSMContext):
    async with state.proxy() as changedData:
        changedData['fio'] = message.text

    chat_id = message.chat.id
    full_name = changedData['fio'].split(' ')
    first_name = full_name[0]
    last_name = full_name[1]
    db_manager.change_name(chat_id, first_name, last_name)
    user_state = db_manager.is_admin(chat_id)
    markup = userMarkup if not user_state else adminMarkup
    await state.finish()
    await bot.send_message(chat_id, successChangeText, reply_markup=markup)


@dp.message_handler(state=SetUserData.email_set)
async def process_set_email(message: types.Message, state: FSMContext):
    async with state.proxy() as changedData:
        changedData['email'] = message.text

    chat_id = message.chat.id
    db_manager.change_email(chat_id, changedData['email'])
    user_state = db_manager.is_admin(chat_id)
    markup = userMarkup if not user_state else adminMarkup
    await state.finish()
    await bot.send_message(chat_id, successChangeText, reply_markup=markup)


@dp.message_handler(state=SetUserData.phone_set)
async def process_set_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as changedData:
        changedData['phone'] = message.text

    chat_id = message.chat.id
    db_manager.change_phone(chat_id, changedData['phone'])
    user_state = db_manager.is_admin(chat_id)
    markup = userMarkup if not user_state else adminMarkup
    await state.finish()
    await bot.send_message(chat_id, successChangeText, reply_markup=markup)

