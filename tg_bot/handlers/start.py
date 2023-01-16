import sqlite3

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from tg_bot.services.db.postgresql import PDatabase
from tg_bot.services.db.sqllite import Database

db = Database()
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    try:
        db.add_user(id=message.from_user.id,
                    name=name)
    except sqlite3.IntegrityError as err:
        print(err)
    count = db.count_users()[0]
    await message.answer(
        "\n".join(
            [
                f'Привет, {message.from_user.full_name}!',
                f'Ты был занесен в базу',
                f'В базе <b>{count}</b> пользователей',
            ]))
def register_bot_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=['start'])
