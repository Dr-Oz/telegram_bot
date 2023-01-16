from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from tg_bot.services.db.sqllite import Database


async def add_email(message: Message, state: FSMContext):
    await message.answer('Пришлите мне свой емейл')
    await state.set_state('email')

async def enter_email(message: Message, state: FSMContext):
    email = message.text
    db = Database()
    db.update_user_email(email=email, id=message.from_user.id)
    user = db.select_user(id=message.from_user.id)
    await message.answer(f'Данные были обновлены. Запись в бд: {user}')
    await state.finish()

def register_add_email(dp: Dispatcher):
    dp.register_message_handler(add_email, Command('email'))
    dp.register_message_handler(enter_email, state='email')