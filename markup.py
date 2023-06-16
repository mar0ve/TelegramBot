from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#---Registration---

btnRegistration = KeyboardButton('Регистрация')
regMarkup = ReplyKeyboardMarkup(resize_keyboard=True).add(btnRegistration)

#---User---
btnStartWork = KeyboardButton('Начать работу')
btnEndWork = KeyboardButton("Закончить работу")
btnReport = KeyboardButton('Отчет')
btnReportAll = KeyboardButton('Полный отчет')
userMarkup = ReplyKeyboardMarkup(resize_keyboard=True).add(btnStartWork, btnEndWork)

#