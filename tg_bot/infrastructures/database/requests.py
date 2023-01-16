import asyncio
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from tg_bot.infrastructures.database.function.items import add_item
from tg_bot.infrastructures.database.modules.item import Item


async def add_items(session: AsyncSession):
    await add_item(session, name="ASUS",
                   category_name="🔌 Электроника", category_code="Electronics",
                   subcategory_name="🖥 Компьютеры", subcategory_code="PCs",
                   price=100, photo="-")
    await add_item(session, name="DELL",
                   category_name="🔌 Электроника", category_code="Electronics",
                   subcategory_name="🖥 Компьютеры", subcategory_code="PCs",
                   price=100, photo="-")
    await add_item(session, name="Apple",
                   category_name="🔌 Электроника", category_code="Electronics",
                   subcategory_name="🖥 Компьютеры", subcategory_code="PCs",
                   price=100, photo="-")
    await add_item(session, name="Iphone",
                   category_name="🔌 Электроника", category_code="Electronics",
                   subcategory_name="☎️ Телефоны", subcategory_code="Phones",
                   price=100, photo="-")
    await add_item(session, name="Xiaomi",
                   category_name="🔌 Электроника", category_code="Electronics",
                   subcategory_name="☎️ Телефоны", subcategory_code="Phones",
                   price=100, photo="-")
    await add_item(session, name="PewDiePie",
                   category_name="🛍 Услуги Рекламы", category_code="Ads",
                   subcategory_name="📹 На Youtube", subcategory_code="Youtube",
                   price=100, photo="-")
    await add_item(session, name="Топлес",
                   category_name="🛍 Услуги Рекламы", category_code="Ads",
                   subcategory_name="📹 На Youtube", subcategory_code="Youtube",
                   price=100, photo="-")
    await add_item(session, name="Орлёнок",
                   category_name="🛍 Услуги Рекламы", category_code="Ads",
                   subcategory_name="🗣 На Вконтакте", subcategory_code="VK",
                   price=100, photo="-")
    await add_item(session, name="МДК",
                   category_name="🛍 Услуги Рекламы", category_code="Ads",
                   subcategory_name="🗣 На Вконтакте", subcategory_code="VK",
                   price=100, photo="-")
    await session.commit()


loop = asyncio.get_event_loop()
url = URL.create(
    drivername="postgresql+asyncpg",  # driver name = postgresql + the library we are using
    username='postgres',
    password='!Cpa2019!',
    host='localhost',
    database='tg_item',
    port=5432
)

engine = create_async_engine(url, echo=True, future=True)
session = AsyncSession(bind=engine)
loop.run_until_complete(add_items(session))