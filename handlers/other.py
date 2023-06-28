from aiogram.utils.exceptions import MessageNotModified
from aiogram import types, Dispatcher
from local_server import dp
import json
    

async def check_spam(message: types.Message):
    # Wczytanie pliku JSON
    with open("config.json", "r") as f:
        config = json.load(f)
    # Sprawdzanie słów kluczowych w treści wiadomości
    for keyword in config["spam_keywords"]:
        if keyword.lower() in message.text.lower():
            # Wykryto spam
            try:
                await message.delete()
                await message.answer("Wykryto spam w tej wiadomości.")
            except MessageNotModified:
                pass
            return

    # Wiadomość jest wolna od spamu
    try:
        await message.reply("Nie posiadam takiej komendy!")
    except MessageNotModified:
        pass

# Obsługa zdarzeń wiadomości
async def handle_message(message: types.Message):
    # Sprawdzenie spamu
    await check_spam(message)

# Function of register commands bots
def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(handle_message)