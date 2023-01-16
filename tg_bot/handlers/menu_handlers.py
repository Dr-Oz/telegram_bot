from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.infrastructures.database.function.items import get_item
from tg_bot.keyboards.inline.menu_keyboards import categories_keyboard, subcategories_keyboard, items_keyboard, \
    item_keyboard, menu_cd


async def show_menu(message: types.Message, session: AsyncSession, ):
    await list_categories(message, session)

async def list_categories(message: Union[types.Message, types.CallbackQuery], session: AsyncSession, **kwargs):
    markup = await categories_keyboard(session)
    if isinstance(message, types.Message):
        await message.answer('Смотри что у нас есть:', reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)

async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)
    await callback.message.edit_reply_markup(markup)

async def list_items(callback: CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category=category, subcategory=subcategory)
    await callback.message.edit_text('Cмотри что у нас есть', reply_markup=markup)

async def show_item(callback: CallbackQuery, category, subcategory, item_id):
    markup = await item_keyboard(category, subcategory, item_id)
    item = await get_item(item_id)
    text = f'Купи {item}'
    await callback.message.edit_text(text, reply_markup=markup)

async def navigate(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get('level')
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')
    item_id = callback_data.get('item_id')
    
    levels = {
        '0': list_categories,
        '1': list_subcategories,
        '3': list_items,
        '4': show_item
    }

    current_level_function = levels[current_level]

    await current_level_function(call, category=category, subcategory=subcategory, item_id=item_id)

def register_show_menu(dp: Dispatcher):
    dp.register_message_handler(show_menu, Command('menu'))
    dp.register_callback_query_handler(navigate, menu_cd.filter())