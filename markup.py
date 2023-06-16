from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from text import *

# ---Registration---

btnRegistration = KeyboardButton(regBtnText)
regMarkup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnRegistration)

# ---User---
btnStartWork = KeyboardButton(startBtnText)
btnEndWork = KeyboardButton(endBtnText)
btnReport = KeyboardButton(repBtnText)
btnReportAll = KeyboardButton(fRepBtnText)
userMarkup = ReplyKeyboardMarkup(resize_keyboard=True).add(btnStartWork, btnEndWork, btnReport, btnReportAll)