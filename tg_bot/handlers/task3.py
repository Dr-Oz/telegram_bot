from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from tg_bot.data.items import items
from tg_bot.keyboard import buy_keyboard, buy_callback, like_callback, dislike_callback


async def show_items(message: types.Message):
    for item in items:
        await message.answer_photo(
            photo=item.photo_link,
            caption=item.title,
            reply_markup=buy_keyboard(item_id=item.item_id)
        )

async def buy_items(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    item_id = callback_data.get('item_id')
    await call.bot.edit_message_caption(caption=f'Покупай товар номер {item_id}!', chat_id=call.message.chat.id, message_id=call.message.message_id)

async def like(call: CallbackQuery, callback_data: dict):
    item_id = callback_data.get('item_id')
    await call.answer(text='Тебе понравился этот товар')

async def dislike(call: CallbackQuery, callback_data: dict):
    item_id = callback_data.get('item_id')
    await call.answer(text='Тебе не понравился этот товар')

async def send_photo(message: types.Message):
    await message.bot.set_chat_title()


def register_show_items(dp: Dispatcher):
    dp.register_message_handler(show_items, Command('items'))
    dp.register_callback_query_handler(buy_items, buy_callback.filter(name='fruit'))
    dp.register_callback_query_handler(like, like_callback.filter(name='like'))
    dp.register_callback_query_handler(dislike, dislike_callback.filter(name='dislike'))
    dp.register_message_handler(send_photo, content_types=types.ContentType.PHOTO)