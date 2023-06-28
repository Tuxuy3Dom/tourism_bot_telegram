import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from local_server import dp, bot

from keyboards import client_kb
from keyboards import btn_bk, btn_register_prof
from database import sqlite_users_db

ID = None
lang_en = 'English'
lang_pl = 'Polish'


class FSMUser(StatesGroup):
    id = State()
    user_id = State()
    name = State()
    last_name = State()
    photo = State()
    age = State()
    sex = State()
    location = State()


# Starts create states - profil users
async def create_profil(message: types.Message, state:FSMContext):
    global ID
    ID = message.from_user.id
    if await sqlite_users_db.sql_check_profil_id(ID):
        if await sqlite_users_db.sql_check_choose_lang(lang_en):
            await state.finish()
            await message.reply('You already have a profile!', reply_markup=btn_register_prof)
        elif await sqlite_users_db.sql_check_choose_lang(lang_pl):
            await state.finish()
            await message.answer('Masz już profil!', reply_markup=btn_register_prof)
        else:
            await state.finish()
            await message.reply('You have not selected a language!')
    else:
        async with state.proxy() as data:
            data['id'] = ID
            data['user_id'] = ID
        await FSMUser.name.set()
        if await sqlite_users_db.sql_check_choose_lang(lang_en):
            await message.answer('What`s your name?', reply_markup=btn_bk) 
        elif await sqlite_users_db.sql_check_choose_lang(lang_pl):
            await message.answer('Jak masz na imię?', reply_markup=btn_bk)
        
# Exit machine state
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals='cancel', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        """
        Allow user to cancel any action
        """
        current_state = await state.get_state()
        if current_state is None:
            return

        logging.info('Cancelling state %r', current_state)
        # Cancel state and inform user about it
        await state.finish()
        # And remove keyboard (just in case)
        await message.reply('Cancelled.')

# Downloading the user first response
async def load_name(message: types.Message, state:FSMContext):
    """
        This handler will be saved user name when user send `text name`
    """
    if message.text == 'Back':
        await FSMUser.name.set()
        await message.answer('What`s your name?', reply_markup=btn_bk)
    else:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMUser.next()
        if await sqlite_users_db.sql_check_choose_lang(lang_en):
            await message.answer("What`s your last name?", reply_markup=btn_bk)
        elif await sqlite_users_db.sql_check_choose_lang(lang_pl):
            await message.answer('Jak masz na nazwisko?', reply_markup=btn_bk)
        

async def load_last_name(message: types.Message, state:FSMContext):
    """
        This handler will be saved user last name when user send `text last name`
    """
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['last_name'] = message.text
        await FSMUser.next()
        if await sqlite_users_db.sql_check_choose_lang(lang_en):
            await message.answer("Include a profile photo!", reply_markup=btn_bk)
        elif await sqlite_users_db.sql_check_choose_lang(lang_pl):
            await message.answer('Dołącz zdjęcie profilowe!', reply_markup=btn_bk)
    
# Downloading the user second response
async def load_photo(message: types.Message, state:FSMContext):
    """
        This handler will be saved user photo when user send `photo`
    """
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMUser.next()
        if await sqlite_users_db.sql_check_choose_lang(lang_en):
            await message.answer("How old are you?", reply_markup=btn_bk)
        elif await sqlite_users_db.sql_check_choose_lang(lang_pl):
            await message.answer('Ile masz lat?', reply_markup=btn_bk)
        
    
# Downloading the moderator's three response
async def load_age(message: types.Message, state:FSMContext):
    """
        This handler will be saved user age when user send `integer age`
    """    
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMUser.next()
        if await sqlite_users_db.sql_check_choose_lang(lang_en):
            male = KeyboardButton('Male')
            female = KeyboardButton('Female')
            await message.answer("Choose your sex: ", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(male, female).add(client_kb.btn_cancel))
        elif await sqlite_users_db.sql_check_choose_lang(lang_pl):
            male = KeyboardButton('Facet')
            female = KeyboardButton('Kobieta')
            await message.answer("Wybierz swoją płeć: ", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(male, female).add(client_kb.btn_cancel))
    

async def load_sex(message: types.Message, state:FSMContext):
    """
        This handler will be saved user sex when user send `choose sex: male or female`
    """    
    if message.from_user.id == ID:
        async with state.proxy() as data:
                data['sex'] = message.text
        await FSMUser.next()
        if message.text == 'Male' or message.text == 'Female':
            if await sqlite_users_db.sql_check_choose_lang(lang_en):
                await message.answer("Enter your location: ", reply_markup=btn_bk)
            elif await sqlite_users_db.sql_check_choose_lang(lang_pl):
                await message.answer('Podaj swoją lokalizację:', reply_markup=btn_bk) 
        elif message.text == 'Facet' or message.text == 'Kobieta':
            if await sqlite_users_db.sql_check_choose_lang(lang_en):
                await message.answer("Enter your location: ", reply_markup=btn_bk)
            elif await sqlite_users_db.sql_check_choose_lang(lang_pl):
                await message.answer('Podaj swoją lokalizację:', reply_markup=btn_bk) 
        else: 
            if await sqlite_users_db.sql_check_choose_lang(lang_en):
                return await message.reply('There is no such gender, please enter again!', reply_markup=btn_bk)
            elif await sqlite_users_db.sql_check_choose_lang(lang_pl):
                return await message.reply('Nie ma takiej płci, wprowadź ponownie!', reply_markup=btn_bk) 
            

# Downloading the moderator's three response
async def load_location(message: types.Message, state:FSMContext):
    """
        This handler will be saved user location when user send `allowed user location`
    """    
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['location'] = message.text
        
        await sqlite_users_db.sql_add_profil(state)
    
        # Finish our state of the machine and clear our data
        await state.finish()
        if await sqlite_users_db.sql_check_choose_lang(lang_en):
            await message.answer('Profile created: ', reply_markup=btn_register_prof) 
        elif await sqlite_users_db.sql_check_choose_lang(lang_pl):
            await message.answer('Profil utworzony: ', reply_markup=btn_register_prof) 

        await sqlite_users_db.sql_read_profil(ID, message)


def register_handlers_profil_user(dp : Dispatcher):
    dp.register_message_handler(create_profil, commands='create_profil', state=None)
    dp.register_message_handler(cancel_handler, state="*", commands="cancel")
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(load_name, state=FSMUser.name)
    dp.register_message_handler(load_last_name, state=FSMUser.last_name)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMUser.photo)
    dp.register_message_handler(load_age, state=FSMUser.age)
    dp.register_message_handler(load_sex, state=FSMUser.sex)
    dp.register_message_handler(load_location, state=FSMUser.location)