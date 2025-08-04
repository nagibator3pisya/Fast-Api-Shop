from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.models import Product, Category, CartItem
from app.schemas.CartItem import CartItemCreate


async def all_product(session: AsyncSession):
    result = await session.execute(select(Product))
    return result.scalars().all()


async def all_category(session: AsyncSession):
    result = await session.execute(select(Category))
    return result.scalars().all()

# Корзина


async def my_cart_all(session: AsyncSession):
    result = await session.execute(select(CartItem))
    return result.scalars().all()


async def add_to_cart(session: AsyncSession, schemas: CartItemCreate):
    cart_items = CartItem(**schemas.model_dump())
    session.add(cart_items)
    await session.commit()
    await session.refresh(cart_items)
    return cart_items
