from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat, BotCommandScopeAllGroupChats, \
    BotCommandScopeAllChatAdministrators, BotCommandScopeChatAdministrators, BotCommandScopeChatMember, \
    BotCommandScopeAllPrivateChats


# STARTING_COMMANDS = {
#     'ru': [],
#     'en': [],
#     'de': [],
#     'fr': []
# }


async def default_commands(bot: Bot):
    """
    Назначает стандартные команды бота во всех чатах.

    :param bot: экземпляр бота, которым будет выполняться команда.
    :return: Возвращает True в случае успешного выполнения.
    """
    return await bot.set_my_commands(
        commands=[
            BotCommand('change_private_commands', 'Изменить команды в личных чатах'),
            BotCommand('change_admin_commands', 'Изменить команды админов групповых чатов'),
            BotCommand('command_default_1', 'Стандартная команда 1'),
            BotCommand('command_default_2', 'Стандартная команда 2'),
            BotCommand('command_default_3', 'Стандартная команда 3'),
            BotCommand('command_default_4', 'Стандартная команда 4'),
        ],
        scope=BotCommandScopeDefault()
    )

# создаем стартовые комманды если юзер с ботом особенно провзаимодествовал, то ему особые комманды
async def set_starting_commands(bot: Bot, chat_id: int):
        STARTING_COMMANDS={
         'ru': [
            BotCommand('start', 'Начать заново'),
            BotCommand('get_commands', 'Получить список комманд'),
            BotCommand('reset_commands', 'Сбросить список комманд')

         ],
         'en': [
             BotCommand('start', 'Starting'),
             BotCommand('get_commsnds', 'Get commands list'),
             BotCommand('reset_commands', 'Reset commands list')
         ]
        }

        for language_code, commands in STARTING_COMMANDS.items():
            await bot.set_my_commands(
                commands=commands,
                scope=BotCommandScopeChat(chat_id),
                language_code=language_code
            )

    # передаем стардантные команды для групп куда может быть добавлен бот
async def set_all_group_command(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('start', 'Информация о боте'),
            BotCommand('report', 'Пожаловаться на пользователя'),
        ],
        scope=BotCommandScopeAllGroupChats()
    )

async def set_all_chat_admins_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('ro', 'Мут пользователя'),
            BotCommand('ban', 'Забанить пользователя'),
            BotCommand('change_commands', 'Изменить команды в этом чате')
        ],
        scope=BotCommandScopeAllChatAdministrators()
    )
    # если мы хотим назначить команды только для администраторов определнного группового чата

async def set_chat_admins_commands(bot: Bot, chat_id: int):
    return await bot.set_my_commands(
        commands=[
            BotCommand('ro', 'Мут пользователя'),
            BotCommand('ban', 'Забанить пользователя'),
            BotCommand('reset_commands', 'Сбросить команды')
        ],
        scope=BotCommandScopeChatAdministrators(chat_id)
    )

    # делаем команды для какого то одного учатстника определенного чата

async def set_chat_member_commands(bot: Bot, chat_id, user_id):
    return await bot.set_my_commands(
        commands=[BotCommand('promote', 'Повысить до админа')],
        scope=BotCommandScopeChatMember(chat_id, user_id)
    )

async def set_all_private_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[BotCommand('account', 'Настройки аккаунта')],
        scope=BotCommandScopeAllPrivateChats()
    )