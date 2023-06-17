from aiogram import executor, types
from aiogram.dispatcher import FSMContext

import markup as nav
from config import dp, db_manager, bot
from text import *
from fsm import AwaitMessages, SetUserData
import func


@dp.message_handler(commands=['start', ])
async def handle_start(message: types.Message):
    chat_id = message.chat.id
    user = db_manager.check_user(chat_id)

    if user is None:
        await bot.send_message(chat_id,
                               regPress, reply_markup=nav.regMarkup)

    else:
        await bot.send_message(chat_id,
                               alreadyReg, reply_markup=nav.userMarkup)


@dp.message_handler()
async def handle_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user = db_manager.check_user(chat_id)

    if user is None:
        if message.text == regBtnText:
            await bot.send_message(chat_id, regWelcome)
            await state.set_state(AwaitMessages.fio_add)

    else:
        user_state = db_manager.is_admin(chat_id)
        markup = nav.userMarkup if not user_state else nav.adminMarkup

        if message.text == startBtnText:
            db_manager.start_workday(user[0])
            await bot.send_message(chat_id, sWorkTypeMessage,
                                   reply_markup=markup)

        elif message.text == endBtnText:
            db_manager.end_workday(user[0])
            await bot.send_message(chat_id, eWorkTypeMessage,
                                   reply_markup=markup)

        elif message.text == repBtnText:
            report = func.print_per_logs(chat_id)

            await bot.send_message(chat_id, report,
                                   reply_markup=markup)

        elif message.text == fRepBtnText:
            report = func.print_all_logs()

            await bot.send_message(chat_id, report,
                                   reply_markup=markup)

        elif message.text == usrProfBtnText:
            profile = db_manager.user_profile(chat_id)
            first_name, last_name, email, phone = profile
            await bot.send_message(chat_id, f"{first_name} {last_name}\nEmail: {email}\nТелефон: {phone}",
                                   reply_markup=markup)

        elif message.text == dataChangeBtnText:
            await bot.send_message(chat_id, "Режим редактирования.", reply_markup=nav.edtProfileMarkup)

        elif message.text == nameBtnText:
            await bot.send_message(chat_id, "Введите новые Имя и Фамилию (Имя Фамилия):",
                                       reply_markup=nav.edtProfileMarkup)
            await state.set_state(SetUserData.fio_set)

        elif message.text == emailBtnText:
            await bot.send_message(chat_id, "Введите новый email:",
                                       reply_markup=nav.edtProfileMarkup)
            await state.set_state(SetUserData.email_set)

        elif message.text == phoneBtnText:
            await bot.send_message(chat_id, "Введите новый номер телефона:",
                                       reply_markup=nav.edtProfileMarkup)
            await state.set_state(SetUserData.phone_set)
        elif message.text == prevNavBtnText:
            await bot.send_message(chat_id, "Режим работы.", reply_markup=markup)

        elif message.text == dep1BtnText:
            users = db_manager.show_all_users(dep1BtnText)

            if not users:
                await bot.send_message(chat_id, f"Сотрудников из отдела - {dep1BtnText} не найдено.",
                                       reply_markup=markup)
            else:
                report = func.set_department_logs(users)
                await bot.send_message(chat_id, report, reply_markup=markup)

        elif message.text == dep2BtnText:
            users = db_manager.show_all_users(dep2BtnText)

            if not users:
                await bot.send_message(chat_id, f"Сотрудников из отдела - {dep2BtnText} не найдено.",
                                       reply_markup=markup)
            else:
                report = func.set_department_logs(users)
                await bot.send_message(chat_id, report, reply_markup=markup)

        elif message.text == dep3BtnText:
            users = db_manager.show_all_users(dep3BtnText)

            if not users:
                await bot.send_message(chat_id, f"Сотрудников из отдела - {dep3BtnText} не найдено.",
                                       reply_markup=markup)
            else:
                report = func.set_department_logs(users)
                await bot.send_message(chat_id, report, reply_markup=markup)

        elif message.text == emplInfoBtnText:
            await bot.send_message(chat_id, "Выберите отдел: ", reply_markup=nav.departmentsMarkup)


if __name__ == '__main__':
    executor.start_polling(dp)
