from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

buy_callback = CallbackData('buy', 'name', 'item_id')
like_callback = CallbackData('like', 'name', 'item_id')
dislike_callback = CallbackData('dislike', 'name', 'item_id')

def buy_keyboard(item_id):

    buy_rate_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                    InlineKeyboardButton(text="Купить товар", callback_data=buy_callback.new(name='fruit', item_id=f'{item_id}'))
            ],
            [
                    InlineKeyboardButton(text="👍", callback_data=like_callback.new(name='like', item_id=f'{item_id}')),
                    InlineKeyboardButton(text="👎", callback_data=dislike_callback.new(name='dislike', item_id=f'{item_id}'))
            ],
            [
                    InlineKeyboardButton(text="Поделиться с другом", switch_inline_query=f'{item_id}')
            ]
        ]
    )
    return buy_rate_keyboard