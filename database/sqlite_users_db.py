import sqlite3 as sq
from local_server import bot


# Tworzenie połączenia z bazą danych SQLite3
def user_start():
    global base, cur
    base = sq.connect('users_data.db')
    cur = base.cursor()
    if base: 
        print('Data base users connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS users_lang(id INTEGER PRIMARY KEY, language TEXT)')
    base.commit()

    base.execute('CREATE TABLE IF NOT EXISTS users_profils(\
                 id INTEGER PRIMARY KEY,\
                 user_id INTEGER,\
                 name TEXT,\
                 last_name TEXT,\
                 photo TEXT,\
                 age TEXT,\
                 sex TEXT,\
                 location TEXT,\
                FOREIGN KEY (user_id) REFERENCES users_lang (id))')
    base.commit()


async def sql_add_lang(user_id, language):
    cur.execute('INSERT INTO users_lang VALUES (?, ?)', (user_id, language,))
    base.commit()


async def sql_check_lang_id(user_id):
    cur.execute('SELECT id FROM users_lang WHERE id = ?', (user_id,))
    return cur.fetchone()


async def sql_check_choose_lang(lang):
    cur.execute('SELECT language FROM users_lang WHERE language = ?', (lang,))
    return cur.fetchone()


async def sql_update_choose_lang(user_id, new_lang):
    cur.execute(f'UPDATE users_lang SET language = {new_lang} WHERE id = ?', (user_id, ))
    base.commit()
    return cur.fetchone()


async def sql_check_choose_lang_id():
    for row in cur.execute('SELECT id, language FROM users_lang ORDER BY id'):
        return print(row)


async def sql_add_profil(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO users_profils VALUES (?, ?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_check_profil_id(user_id):
    cur.execute('SELECT id FROM users_profils WHERE id = ?', (user_id, ))
    return cur.fetchone()


async def sql_read_profil(user_id, message):
    lang_en = 'English'
    lang_pl = 'Polish'
    if await sql_check_choose_lang(lang_en):
        for ret in cur.execute('SELECT * FROM users_profils WHERE id = ?', (user_id, )).fetchall():
            await bot.send_photo(message.from_user.id, ret[4], f'*{ret[2]} {ret[3]}*\n\n*Age*: {ret[5]},\n*Sex*: {ret[6]},\n*City*: {ret[-1]}', parse_mode="Markdown")
    elif await sql_check_choose_lang(lang_pl):
        for ret in cur.execute('SELECT * FROM users_profils WHERE id = ?', (user_id, )).fetchall():
            await bot.send_photo(message.from_user.id, ret[4], f'*{ret[2]} {ret[3]}*\n\n*Wiek*: {ret[5]},\n*Płeć*: {ret[6]},\n*Miasto*: {ret[-1]}', parse_mode="Markdown")


async def sql_delete_profil(user_id, message):
    cur.execute('DELETE FROM users_profils WHERE id = ?', (user_id, )).fetchall()
    base.commit()
    await message.answer('Delete profile success')