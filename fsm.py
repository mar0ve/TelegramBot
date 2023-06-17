from config import State, StatesGroup, types, FSMContext, db_manager, userMarkup, dp
from text import *
from datetime import datetime


class AwaitMessages(StatesGroup):
    fio_add = State()
    phone_add = State()
    email_add = State()
    tel_link_add = State()


@dp.message_handler(state=AwaitMessages.fio_add)
async def process_fio_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fio'] = message.text

    await message.answer('Введите телефон: ')
    await AwaitMessages.phone_add.set()


@dp.message_handler(state=AwaitMessages.phone_add)
async def process_phone_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

    await message.answer('Введите email: ')
    await AwaitMessages.email_add.set()


@dp.message_handler(state=AwaitMessages.email_add)
async def process_email_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text

    chat_id = message.chat.id
    full_name = data['fio'].split(' ')
    first_name = full_name[0]
    last_name = full_name[1]
    phone = data['phone']
    email = data['email']
    db_manager.register_user(chat_id, first_name, last_name, email, phone, datetime.now(), 'user')
    await state.finish()
    await message.answer(applyReg, reply_markup=userMarkup)
