from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.models import Product, Category


async def all_product(session: AsyncSession):
    result = await session.execute(select(Product))
    return result.scalars().all()


async def all_category(session: AsyncSession):
    result = await session.execute(select(Category))
    return result.scalars().all()
