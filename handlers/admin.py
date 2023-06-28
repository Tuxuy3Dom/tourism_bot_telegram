from local_server import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging

from database import sqlite_admin_db
from keyboards import admin_kb

ID = None

class FSMAdmin(StatesGroup):
    title = State()
    photo = State()
    description = State()
    location = State()
    

# Retrieve the moderator's user ID
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Admin panels are available!', reply_markup=admin_kb.btn_case_admin)
    await message.delete()
    

# Start in work save new places in tourism list
async def cmd_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.title.set()
        await message.reply('Wpisz nazwe miejsca turystycznego: ')
    else:
        await message.reply('You don`t have access to the admin panels!')


# Exit machine state
@dp.message_handler(state="*", commands="Cancel")
@dp.message_handler(Text(equals='Cancel', ignore_case=True), state="*")
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


# Downloading the moderator's first response
async def load_title(message: types.Message, state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply("Dodaj zdjęcie tego miejsca!")
    

# Downloading the moderator's second response
async def load_photo(message: types.Message, state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply("Napisz coś o tym miejscu: ")
    

# Downloading the moderator's three response
async def load_description(message: types.Message, state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply("Podaj linka do lokalizacji danego miejsca: ")
    

# Downloading the moderator's three response
async def load_location(message: types.Message, state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['location'] = message.text
        
        await sqlite_admin_db.sql_add_command(state)
        # Finish our state of the machine and clear our data
        await state.finish()
        await message.answer('Dodanie nowego miejsca udało się.')


# Function of register commands bots for admins
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands='new_place', state=None)
    dp.register_message_handler(cancel_handler, state="*", commands="Cancel")
    dp.register_message_handler(cancel_handler, Text(equals='Cancel', ignore_case=True), state="*")
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(load_title, state=FSMAdmin.title)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_location, state=FSMAdmin.location)
