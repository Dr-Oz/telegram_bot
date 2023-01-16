from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from config import load_config


class PDatabase:
    def __init__(self):
        # пул соединений Union означает несколько значений
        self.pool: Union[Pool, None] = None
        self.config = load_config()
    # будем создавать подключение и пул с новыми данными
    async def create(self):

        self.pool = await asyncpg.create_pool(
            user=self.config.db.user,
            password=self.config.db.password,
            host=self.config.db.host,
            database=self.config.db.database

        )
    # создаем запросы, command = команда, доп аргументы что именно хотим сделать
    # Fetch собирает все данные после выполнения запроса, fetchval = какое то одно значение
    # fetchrow - выгружает один список не вложенный в другой
    # execute если не хотим возвращать данные а просто выполнить команду
    async def execute(self, command, *args, fetch: bool = False, fetchval: bool = False, fetchrow: bool = False, execute: bool = False):
        # создаем асинхронный менедежер контекста
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result
    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INT NOT NULL,
            full_name VARCHAR(255) NOT NULL,
            username VARCHAR(255) NULL,
            telegram_id BIGINT NOT NULL,
            );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND".join([
            f'{item} = ${num}' for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values()) # возвращаем кортеж который будет раскрываться в execute

    async def add_user(self, full_name, username, telegram_id):
        sql = 'INSERT INTO Users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *' # вернет все столбцы пользователей
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = 'SELECT * FROM Users'
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = 'SELECT (COUNT(*) FROM Users'
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = 'UPDATE Users SET username=$1 WHERE telegram_id=$2'
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute('DROP TABLE Users', execute=True)

