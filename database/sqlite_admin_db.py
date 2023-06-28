import sqlite3 as sq
from local_server import bot

def sql_start():
    global base, cur
    base = sq.connect('admin_base.db')
    cur = base.cursor()
    if base: 
        print('Data base admin connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS places(title TEXT PRIMARY KEY, photo TEXT, description TEXT, location TEXT)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO places VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM places').fetchall():
        await bot.send_photo(message.from_user.id, ret[1], f"*{ret[0]}*\n\n*Opis:* {ret[2]}\n\n*Link do lokalizacji:* {ret[-1]}", parse_mode="Markdown")

async def perform_search():
    """
    This function created for search tourist places after writen city or read city with profil user and show tourism list, 
    Where did he point to your city.
    """
    pass