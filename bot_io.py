import markup as nav
from config import *
from text import *
from fsm import AwaitMessages


@dp.message_handler(commands=['start',])
async def handle_start(message: types.Message):
    chat_id = message.chat.id
    user = db_manager.check_user(chat_id)

    if user is None:
        await bot.send_message(chat_id,
                               'Нажмите на кнопку Регистрация', reply_markup=nav.regMarkup)

    else:
        await bot.send_message(chat_id,
                               alreadyReg, reply_markup=nav.userMarkup)


@dp.message_handler()
async def handle_message(message: types.Message, state: FSMContext):
    #define user
    chat_id = message.chat.id
    user = db_manager.check_user(chat_id)

    if user is None:
        if message.text == regBtnText:
            await message.answer(regWelcome)
            await state.set_state(AwaitMessages.fio_add)

    else:
        user_state = db_manager.is_admin(chat_id)
        markup = nav.userMarkup if user_state is False else nav.adminMarkup
        if message.text == startBtnText:
            db_manager.start_workday(user[0])
            await bot.send_message(chat_id, sWorkTypeMessage,
                                   reply_markup=markup)

        elif message.text == endBtnText:
            db_manager.end_workday(user[0])
            await bot.send_message(chat_id, eWorkTypeMessage,
                                   reply_markup=markup)

        elif message.text == repBtnText:
            work_logs = db_manager.print_info(chat_id)
            report = "Отчет о пребывании на работе:\n\n"
            for log in work_logs:
                first_name = log[0]
                last_name = log[1]
                start_time = log[2]
                end_time = log[3] if log[3] is not None else "В процессе"
                report += f"Имя: {first_name}\nФамилия: {last_name}\nНачало дня: {start_time}\nКонец дня: {end_time}\n\n"

            await bot.send_message(chat_id, report,
                                   reply_markup=markup)

        elif message.text == fRepBtnText:
            work_logs = db_manager.print_all_info()
            report = "Отчет о пребывании на работе:\n\n"
            for log in work_logs:
                first_name = log[0]
                last_name = log[1]
                start_time = log[2]
                end_time = log[3] if log[3] is not None else "В процессе"
                report += f"Имя: {first_name}\nФамилия: {last_name}\nНачало дня: {start_time}\nКонец дня: {end_time}\n\n"

            await bot.send_message(chat_id, report,
                                   reply_markup=markup)

        elif message.text == usrProfBtnText:
            profile = db_manager.user_profile(chat_id)
            full_name = str(profile[2]) + ' ' + str(profile[3])
            email = profile[4]
            phone = profile[5]
            await bot.send_message(chat_id, f"{full_name}\nEmail: {email}\nТелефон: {phone}",
                                   reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp)