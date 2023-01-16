from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from sqlalchemy.orm import aliased

from tg_bot.infrastructures.database.modules.item import Item
from tg_bot.infrastructures.database.modules.users import User
from sqlalchemy import insert, select, update, func, and_


async def add_item(session: AsyncSession,
                   name,
                   category_name,
                   category_code,
                   subcategory_name,
                   subcategory_code,
                   price,
                   photo):
    stmt = insert(Item).values(
        name=name,
        category_name=category_name,
        category_code=category_code,
        subcategory_name=subcategory_name,
        subcategory_code=subcategory_code,
        price=price,
        photo=photo,
    )
    await session.execute(stmt)


async def get_categories(session: AsyncSession) -> list[Item]:
    statement = select(
        Item.category_name
    )
    result: AsyncResult = await session.scalars(statement)
    return result.unique().all()


async def get_subcategories(session: AsyncSession, category) -> list[Item]:
    statement = select(
        Item.subcategory_name
    ).where(
        Item.category_code == category
    )
    result: AsyncResult = await session.scalars(statement)
    return result.unique().all()


async def count_items(session: AsyncSession, category_code, subcategory_code=None) -> int:
    conditions = [Item.category_code == category_code]
    if subcategory_code:
        conditions.append(Item.subcategory_code == subcategory_code)
    stmt = select(
        func.count(Item.id)
    ).where(
        *conditions
    )
    result: AsyncResult = await session.scalars(stmt)
    return result.unique().all()



async def get_items(session: AsyncSession, category_code, subcategory_code) -> list[Item]:
    statement = select(
        Item.subcategory_name
    ).where(
        and_(Item.category_code == category_code, Item.subcategory_code == subcategory_code)
    )
    result: AsyncResult = await session.scalar(statement)
    return result.unique().all()

async def get_item(session: AsyncSession, item_id):
    statement = select(
        Item
    ).where(
        Item.id == item_id
    ).order_by(
        Item.created_at.desc()
    )
    result: AsyncResult = await session.scalars(statement)
    return result.first()