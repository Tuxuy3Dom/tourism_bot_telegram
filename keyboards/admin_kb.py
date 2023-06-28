from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove 

btn_load = KeyboardButton('/new_place')
btn_delete = KeyboardButton('/delete')

btn_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(btn_load, btn_delete)