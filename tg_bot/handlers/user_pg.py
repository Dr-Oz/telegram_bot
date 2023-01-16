

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import quote_html
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.infrastructures.database.function.users import create_user, update_users
from tg_bot.infrastructures.database.modules.users import User


async def user_start(message: Message, session: AsyncSession):
    user = await session.get(User, message.from_user.id)

    if not user:
        await create_user(
            session,
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            language_code=message.from_user.language_code,
        )
        await session.commit()

    user = await session.get(User, message.from_user.id)
    user_info = (f"{user.full_name} (@{user.username}).\n"
                 f"Language: {user.language_code}.\n"
                 f"Created at: {user.created_at}.")

    await message.reply("Hello, user. \n"
                        "Your info is here: \n\n"
                        f"{user_info}")


async def add_email_pg(message: Message, state: FSMContext):
    await message.answer('Пришлите мне свой телефон')
    await state.set_state('phone')


async def enter_email_pg(message: Message, state: FSMContext, session: AsyncSession):
    phone_number = message.text
    phone = quote_html(phone_number)
    print(phone)
    await update_users(session, telegram_id=message.from_user.id, phone_number=phone
    )
    await session.commit()
    user = await session.get(User, message.from_user.id)
    await message.answer(f'Данные были обновлены. Запись в бд: {user.full_name}')
    await state.finish()



def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(add_email_pg, Command('phone'))
    dp.register_message_handler(enter_email_pg, state='phone')