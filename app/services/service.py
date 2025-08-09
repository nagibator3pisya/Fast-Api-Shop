from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

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
    # 1. Проверка остатка товара
    query = select(Product).where(Product.id == schemas.product_id)
    result = await session.execute(query)
    product = result.scalars().first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )

    if product.quantity < schemas.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"На складе осталось только {product.quantity} шт."
        )


    # уменьшение остатка на складе
    product.quantity -= schemas.quantity
    session.add(product)


    # 2. Добавление в корзину
    cart_item = CartItem(
        **schemas.model_dump(),
        user_id=user.id
    )
    session.add(cart_item)
    await session.commit()
    await session.refresh(cart_item)

    return cart_item



async def remove_from_cart(session: AsyncSession, cart_item_id: int, user: User):
    # 1. Поиск товара в карзине
    query = select(CartItem).where(
        CartItem.id == cart_item_id,
        CartItem.user_id == user.id
    )
    result = await session.execute(query)
    cart_item = result.scalars().first()

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар в корзине не найден"
        )

    # 2. Возвращаем товар на склад
    query = select(Product).where(Product.id == cart_item.product_id)
    result = await session.execute(query)
    product = result.scalars().first()

    if product:
        product.quantity += cart_item.quantity
        session.add(product)

    # 3. Удаляем из корзины
    await session.delete(cart_item)
    await session.commit()

    return {"detail": "Товар удалён из корзины и резерв снят"}
