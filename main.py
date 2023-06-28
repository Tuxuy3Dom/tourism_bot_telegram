from aiogram.utils import executor
from local_server import dp
from database import sqlite_admin_db, sqlite_users_db
from handlers import admin, choose_lang, other, profil_user, user

# Function for displaying a message that the bot is online
async def on_startup(_):
    print('This bot is online...')
    # The connection to the database will still be displayed here
    sqlite_admin_db.sql_start()
    sqlite_users_db.user_start()

if __name__ == "__main__":
    # Registration all handlers for out bot, these commands
    user.register_handlers_user(dp)
    choose_lang.register_handlers_settings_lang(dp)
    profil_user.register_handlers_profil_user(dp)
    admin.register_handlers_admin(dp)
    other.register_handlers_other(dp)
    
    # Start out bot method - for stop, press (Ctrl + C)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
