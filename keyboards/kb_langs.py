from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

btn_en = KeyboardButton('English')
btn_pl = KeyboardButton('Polish')

btn_lang = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_lang.row(btn_en, btn_pl)