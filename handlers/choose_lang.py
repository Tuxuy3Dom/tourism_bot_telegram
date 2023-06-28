# - *- coding: utf- 8 - *-T
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from handlers import profil_user

from local_server import dp
from database import sqlite_users_db

class LanguageState(StatesGroup):
    ENGLISH = State()
    POLISH = State()


# Definition handlers for choosed language
async def choose_lang(message: types.Message):
    """
    This handler will be called when the user selects a language `English or Polish` click button
    """
    await LanguageState.ENGLISH.set()
    await message.answer('Please choose your language: English or Polish')


# Handler for choose english language
async def english_selected(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    language = 'English'
    if await sqlite_users_db.sql_check_lang_id(user_id):
        # Rekord istnieje, możesz podjąć odpowiednie działania
        await state.finish()
        await message.answer('You have selected a language. Now we create the profile click: /create_profil')
    else:
        await sqlite_users_db.sql_add_lang(user_id, language)
        await state.finish()  # Usunięcie stanu
        await message.reply('English has been selected, now we create the profile click: /create_profil')


# Handler for choose polish language
async def polish_selected(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    language = 'Polish'
    if await sqlite_users_db.sql_check_lang_id(user_id):
        # Rekord istnieje, możesz podjąć odpowiednie działania
        await state.finish()
        await message.answer('Masz wybrany język. Teraz tworzymy profil:')
        await profil_user.create_profil(message, state)
    else:
        await sqlite_users_db.sql_add_lang(user_id, language)
        await state.finish()  # Usunięcie stanu
        await message.reply('Wybrałeś język polski. Teraz tworzymy profil:')
        await profil_user.create_profil(message, state)

async def continue_choose_lang(message: types.Message):
    """
    This handler will be changing the communication language while the bot is running when user send '/language'
    """
    await sqlite_users_db.sql_update_choose_lang(message.from_user.id, )

def register_handlers_settings_lang(dp : Dispatcher):
    dp.register_message_handler(english_selected, state="*", commands="english")
    dp.register_message_handler(english_selected, Text(equals='english', ignore_case=True), state="*")
    dp.register_message_handler(polish_selected, state="*", commands="polish")
    dp.register_message_handler(polish_selected, Text(equals='polish', ignore_case=True), state="*")
    dp.register_message_handler(continue_choose_lang, commands=['language'])


