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
btnUsrProfile = KeyboardButton(usrProfBtnText)
btnDataChange = KeyboardButton(dataChangeBtnText)
btnNotification = KeyboardButton(notificationsBtnText)
btnAllUsers = KeyboardButton(emplInfoBtnText)

userMarkup = ReplyKeyboardMarkup(resize_keyboard=True).row(
    btnStartWork, btnEndWork).row(
    btnReport, btnUsrProfile).row(
    btnDataChange, btnAllUsers)

adminMarkup = ReplyKeyboardMarkup(resize_keyboard=True).add(
    btnStartWork, btnEndWork).row(
        btnReport, btnReportAll).add(
        btnUsrProfile).row(
        btnDataChange, btnAllUsers
)

# --- Edit Profile ---
btnName = KeyboardButton(nameBtnText)
btnEmail = KeyboardButton(emailBtnText)
btnPhone = KeyboardButton(phoneBtnText)
btnPrev = KeyboardButton(prevNavBtnText)

edtProfileMarkup = ReplyKeyboardMarkup(resize_keyboard=True).add(
    btnName, btnEmail, btnPhone, btnPrev,
)

# --- Departments ---
btnDep1 = KeyboardButton(dep1BtnText)
btnDep2 = KeyboardButton(dep2BtnText)
btnDep3 = KeyboardButton(dep3BtnText)

departmentsMarkup = ReplyKeyboardMarkup(resize_keyboard=True).add(
    btnDep1, btnDep2, btnDep3,
)
