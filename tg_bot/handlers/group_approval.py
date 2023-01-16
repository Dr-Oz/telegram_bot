import asyncio
import random

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData

approval_cb = CallbackData('chat_join_request', 'approve', 'chat_id')

async def process_chat_invite_request(chat_join_request_handler: ChatJoinRequest, state: FSMContext):
    approve_button = [

            InlineKeyboardButton(text="🐱", callback_data=approval_cb.new(approve='1',
                                                                         chat_id=chat_join_request_handler.chat.id)),
            InlineKeyboardButton(text="🐶", callback_data=approval_cb.new(approve='0',
                                                                         chat_id=chat_join_request_handler.chat.id)),
            InlineKeyboardButton(text="🐬", callback_data=approval_cb.new(approve='0',
                                                                         chat_id=chat_join_request_handler.chat.id))
    ]
    random.shuffle(approve_button)
    await chat_join_request_handler.bot.send_message(
        chat_join_request_handler.from_user.id,
        'Нажмите на кнопку с котиком',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[approve_button])
    )


    #await asyncio.sleep(3)
    # здесь можно сделать проверку есть ли юзер в базе данных или сделать запрос пользователя на оплату или подписаться на канал
    #await chat_join_request_handler.approve() # одобрение
    #await chat_join_request_handler.decline() # неодобрение

    # создаем отсеивание юзерботов
async def approve_callback_group_capthcha(call: CallbackQuery, callback_data: dict):
    await call.message.delete_reply_markup()
    await call.message.answer('Вы были приняты в в группу')
    chat_id = callback_data['chat_id']
    await call.bot.approve_chat_join_request(chat_id, call.from_user.id)

async def decline_callbach_group_capthcha(call: CallbackQuery, callback_data: dict):
    await call.message.delete_reply_markup()
    await call.message.answer('Вы не прошли проверку')

    chat_id = callback_data['chat_id']
    await call.bot.decline_chat_join_request(chat_id, call.from_user.id)


def register_group_approval(dp: Dispatcher):
    dp.register_chat_join_request_handler(process_chat_invite_request)
    dp.register_callback_query_handler(approve_callback_group_capthcha,
                                       approval_cb.filter(approve='1'))
    dp.register_callback_query_handler(decline_callbach_group_capthcha,
                                       approval_cb.filter())