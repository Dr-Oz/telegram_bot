from aiogram import types, Dispatcher, Bot
from aiogram.types import BotCommandScopeChat, Message, BotCommandScopeAllGroupChats, BotCommandScopeAllPrivateChats, \
    BotCommandScopeAllChatAdministrators, BotCommandScopeDefault, ChatType
from aiogram.utils.markdown import quote_html

from tg_bot.services.setting_commands import set_starting_commands, set_chat_admins_commands


async def user_starts(message:types.Message):
    await message.reply('Hello, user!')
    await set_starting_commands(message.bot, message.from_user.id)

async def message_get_commands(message:types.Message):
    no_lang = await message.bot.get_my_commands(scope=BotCommandScopeChat(message.from_user.id))
    no_args = await message.bot.get_my_commands()
    ru_lang = await message.bot.get_my_commands(scope=BotCommandScopeChat(message.from_user.id), language_code='ru')
    # также делаем экранирование символов так так глобально применяется парс мод HTML
    await message.reply("\n\n".join(
        f'<pre>{quote_html(arg)}</>' for arg in (no_lang, no_args, ru_lang)
    ))
async def message_reset_commands(message: Message):
    await message.bot.delete_my_commands(BotCommandScopeChat(message.from_user.id), language_code='ru')
    await message.reply('Команды были удалены')

async def force_reset_all_commands(bot: Bot):
    for language_code in ('ru', 'en', 'ua'):
        for scope in (
            BotCommandScopeAllGroupChats(),
            BotCommandScopeAllPrivateChats(),
            BotCommandScopeAllChatAdministrators(),
            BotCommandScopeDefault()

        ):
            await bot.delete_my_commands(scope, language_code)

async def change_admin_commands(message: Message):
    await set_chat_admins_commands(message.bot, message.chat.id)
    await message.answer('Команды для администраторов для этого чата были изменены')


def register_user_start(dp: Dispatcher):
    dp.register_message_handler(user_starts, commands=['start'], state='*')
    dp.register_message_handler(message_get_commands, commands=['get_commands'])
    dp.register_message_handler(message_reset_commands, commands=['reset_commands'])
    dp.register_message_handler(change_admin_commands, commands=['change_commands'], chat_type=ChatType.SUPERGROUP) # будет нажиматься именно в групповом чате