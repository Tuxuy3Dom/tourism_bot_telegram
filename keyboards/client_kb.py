from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1_start = KeyboardButton('/start')
b2_list = KeyboardButton('/tourist_list')
b3_help = KeyboardButton('/help')

btn_remove = ReplyKeyboardRemove()

# Buttons for file <profile_user.py> - activities with the profile
btn_register_prof = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
btn_profile = KeyboardButton('Profil')
btn_edit_prof = KeyboardButton('Edit profile')
btn_del_prof = KeyboardButton('Delete profile')
# Register previous buttons
btn_register_prof.row(btn_profile,btn_edit_prof, btn_del_prof)

# Buttons for file <profile_user.py> - state machine
btn_bk = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
btn_cancel = KeyboardButton('Cancel')
btn_bk.insert(btn_cancel)

# Buttons begginers
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.row(b1_start, b2_list, b3_help)