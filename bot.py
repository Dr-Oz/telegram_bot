import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from tg_bot.handlers.group_approval import register_group_approval
from tg_bot.handlers.menu_handlers import register_show_menu
from tg_bot.handlers.start import register_bot_start
from tg_bot.handlers.task3 import  register_show_items
from config import load_config
from tg_bot.handlers.user_pg import register_user
from tg_bot.infrastructures.database.function.setup import create_session_pool
from tg_bot.middlewares.database import DatabaseMiddleware
from tg_bot.middlewares.enviiroment import EnvironmentMiddleware
from tg_bot.services.db.update_db import register_add_email

logger = logging.getLogger(__name__)

def register_all_middlewares(dp, config, session_pool):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(DatabaseMiddleware(session_pool=session_pool))

def register_all_filters(dp):
    pass

def register_all_handlers(dp):
    register_show_menu(dp)
    register_user(dp)
    #register_bot_start(dp)
    #register_add_email(dp)
    register_show_items(dp)
    register_group_approval(dp)


#async def set_all_default_commands(bot: Bot):
    # await force_reset_all_commands(bot)
    #await default_commands(bot)
    #await set_all_group_command(bot)
    #await set_all_chat_admins_commands(bot)
    # await set_chat_admins_commands(bot)
    #  await set_chat_member_commands(bot)
    #await set_all_private_commands(bot)
    # просто перечисляем а не подгружаем ничего лишнего



async def main():
    logging.basicConfig(    # конфиг логирования
        level=logging.INFO,  # уровень логирования - здесь 20
        format=u'%(filename)s:%(lineno)d #%(levelname) -8s [%(asctime)s] - %(name)s - %(message)s',
    ) # имя файла, номер строчки, уровень логирования, время
    config = load_config('.env')

    # storage - это машина состояний используется вместе с redis
    storage = MemoryStorage()# если мы хотим использовать
    # оперативную память для машины состояний и переменных
    #db = Database()
    #db = PDatabase()
    #try:
        # db.create_table_users()
        #session_pool = create_session_pool(config.db)
    #except Exception as err:
        #print(err)
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    session_pool = create_session_pool(config.db)

    bot['config'] = config

    register_all_middlewares(dp, config, session_pool)
    register_all_filters(dp)
    register_all_handlers(dp)

    #await set_all_default_commands(bot)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close() # закрываем соединение сторэджа
        await dp.storage.wait_closed() # дожидаемся пока закроется
        await bot.session.close() # закрываем сессию бота


if __name__ == '__main__':
    try:
        asyncio.run(main())  #добавляем корутину функции main
        #keyboardinterrupt - это ctrl + c
    except(KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')