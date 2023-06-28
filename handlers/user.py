# - *- coding: utf- 8 - *-T
"""Users section"""
from aiogram import types, Dispatcher
from local_server import bot
from keyboards import kb_client, btn_lang
from database import sqlite_admin_db, sqlite_users_db
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

from handlers import choose_lang
from keyboards import btn_register_prof

lang_en = 'English'
lang_pl = 'Polish'


async def command_start(message: types.Message):
    """
    This handler will be called when user send `/start` command
    """
    user_id = message.from_user.id
    if await sqlite_users_db.sql_check_lang_id(user_id):
        if await sqlite_users_db.sql_check_choose_lang(lang_en):
            await bot.send_message(user_id, 'Welcome to the tourism bot!\n', reply_markup=btn_register_prof)
        elif await sqlite_users_db.sql_check_choose_lang(lang_pl):
            await bot.send_message(user_id, 'Witamy w bocie turystycznym!\n', reply_markup=btn_register_prof)
    else:
        try:
            await bot.send_message(user_id, 'Welcome to the tourism bot!\n', reply_markup=btn_lang)
        except:
            await message.reply("The first communication with the bot should take place at the user's initiative, as the bot does not have the right to write privately first. Please write to him for communication:\nhttps://t.me/for_tourism_bot") 
        await choose_lang.choose_lang(message)


async def connect_web_app(message: types.Message):
    """
    This handler will be connects the user to the web application when user send `/open`
    """
    url_app = InlineKeyboardMarkup(row_width=1)
    url_app_but = InlineKeyboardButton(text='O jedno marzenie dalej', url='https://t.me/for_tourism_bot/opentravel_blog')
    await message.answer('Open out web page: O jedno marzenie dalej', reply_markup=url_app.add(url_app_but))

async def open_profil(message: types.Message):
    """
    This handler will be displays a profile when user send `Profil`
    """
    user_id = message.from_user.id
    if await sqlite_users_db.sql_check_profil_id(user_id):
        if await sqlite_users_db.sql_check_choose_lang(lang_en):
            await message.answer('Your profil:', reply_markup=ReplyKeyboardRemove())
            await sqlite_users_db.sql_read_profil(user_id, message)
        elif await sqlite_users_db.sql_check_choose_lang(lang_pl):
            await message.answer('Twój profil:', reply_markup=ReplyKeyboardRemove())
            await sqlite_users_db.sql_read_profil(user_id, message)
    else: 
        if await sqlite_users_db.sql_check_choose_lang(lang_en):
            await message.reply(f"You don't have a profile created, create one, /create_profil", reply_markup=ReplyKeyboardRemove())
        elif await sqlite_users_db.sql_check_choose_lang(lang_pl):
            await message.reply(f"Nie masz utworzonego profilu, utwórz go: /create_profil", reply_markup=ReplyKeyboardRemove())
        

async def edit_profil(message: types.Message):
    """
    This handler will be edited profile when user send `Edit profil`
    """
    user_id = message.from_user.id
    pass


async def delete_profil(message: types.Message):
    """
    This handler will be delete profile when user send `Delete profile`
    """
    user_id = message.from_user.id
    await sqlite_users_db.sql_delete_profil(user_id, message)


async def search_places(message: types.Message):
    """
    This handler will be search_places when user send `/search`
    """
    
    # Pobranie zapytania wysłanego przez użytkownika
    query = message.get_args()
    # Wykonaj logikę wyszukiwania miejsc na podstawie zapytania query
    results = sqlite_admin_db.perform_search(query)

    if results:
        response = 'Oto wyniki wyszukiwania: \n'
        for result in results:
            response += f"- {result}\n"
    else:
        response = "Niestety, nie znaleziono żadnych miejsc pasująych do zapytania."

    # Wysłanie odpowiedzi do użytkownika
    await message.reply_text(response)

async def open_tourist_list_places(message: types.Message):
    """
    This handler will be displays a list of tourist places when user send `/all_places`
    """
    await sqlite_admin_db.sql_read(message)
    

async def command_help(message: types.Message):
    """
    This handler will be View all available user functionalities when user send `/help`
    """   
    await message.answer('/start - run works in projects,\n/open - show web app in connects with bot,\n/create_profil - create your profil in bots,\n/all_places - show lists with places for visit\n', reply_markup=btn_register_prof)
    

# Function of register commands bots for users
def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(connect_web_app, commands=['open'])
    dp.register_message_handler(open_profil, Text(equals='profil', ignore_case=True))
    dp.register_message_handler(edit_profil, Text(equals='edit profile', ignore_case=True))
    dp.register_message_handler(delete_profil, Text(equals='delete profile', ignore_case=True))
    dp.register_message_handler(open_tourist_list_places, commands=['all_places'])
    dp.register_message_handler(command_help, commands=['help'])