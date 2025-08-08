from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.model.models import Product, Category, CartItem, User
from app.schemas.CartItem import CartItemCreate


async def all_product(session: AsyncSession):
    result = await session.execute(select(Product))
    return result.scalars().all()


async def all_category(session: AsyncSession):
    result = await session.execute(select(Category))
    return result.scalars().all()

# Корзина


async def my_cart_all(session: AsyncSession,  current_user: User = Depends(get_current_user())):
    result = select(CartItem).where(CartItem.user_id == current_user.id)
    cart_all = await session.execute(result)
    return cart_all.scalars().all()

'''
    stmt = select(Task).where(Task.id == task_id, Task.owner_id == current_user.id)
    result = await session.execute(stmt)
    return result.scalars().first()
'''



async def add_to_cart(session: AsyncSession, schemas: CartItemCreate, user: User):
    cart_items = CartItem(**schemas.model_dump(), user_id=user.id)
    session.add(cart_items)
    await session.commit()
    await session.refresh(cart_items)
    return cart_items
