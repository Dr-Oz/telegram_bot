from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.infrastructures.database.function.items import get_categories, count_items, get_subcategories, get_items

menu_cd = CallbackData("show_menu", "level", "category", "subcategory", "item_id")
buy_item = CallbackData("buy", "item_id")


def make_callback_data(level, category="0", subcategory="0", item_id="0"):
    return menu_cd.new(level=level,
                       category=category, subcategory=subcategory, item_id=item_id)


async def categories_keyboard(session: AsyncSession):
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()

    categories = await get_categories(session)
    for category in categories:
        number_of_items = await count_items(session, category)
        # формируем текст на кнопке
        button_text = f"{category} ({number_of_items} шт)"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category)
        # вставляем в нашу клавиатуру
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    return markup


async def subcategories_keyboard(session: AsyncSession, category):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    subcategories = await get_subcategories(session, category)
    print(subcategories)
    for subcategory in subcategories:
        number_of_items = await count_items(session, category_code=category, subcategory_code=subcategory.subcategory_code)
        button_text = f"{subcategory.subcategory_name} ({number_of_items} шт)"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category, subcategory=subcategory.subcategory_code)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # кнопка назад
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    return markup


async def items_keyboard(category, subcategory):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)  # параметр - количество кнопок в строке

    items = await get_items(category, subcategory)
    for item in items:
        button_text = f"{item.name} {item.price}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category, subcategory=subcategory,
                                           item_id=f"{item.id}")
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # кнопка назад
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category=category)
        )
    )
    return markup


def item_keyboard(category, subcategory, item_id):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text="Купить",
            callback_data=buy_item.new(item_id=item_id)
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category=category, subcategory=subcategory)
        )
    )
    return markup
