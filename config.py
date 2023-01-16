from dataclasses import dataclass
from typing import List
from environs import Env
from sqlalchemy.engine import URL

@dataclass
class DbConfig:
 host: str
 password: str
 user: str
 database: str
 port: int

 def construct_sqlalchemy_url(self, library='asyncpg') -> URL:
        return str(URL.create(
            drivername=f"postgresql+{library}",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        ))

@dataclass
class TgBot:
    token: str
    use_redis: bool

@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig



# функция, которая по запросу будет выгружать конфиг:
def load_config(path: str=None):
    # подгружаем переменное окружение с помощью библиотеки env
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str('BOT_TOKEN'),
            use_redis=env.bool('USE_REDIS'),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('POSTGRES_PASSWORD'),
            user=env.str('POSTGRES_USER'),
            database=env.str('POSTGRES_DB'),
            port=env.int('DB_PORT'),
    ))

