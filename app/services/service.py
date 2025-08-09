from datetime import datetime, timedelta

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
    query = select(Product).where(Product.id == schemas.product_id)
    result = await session.execute(query)
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    if product.quantity < schemas.quantity:
        raise HTTPException(status_code=400, detail=f"На складе осталось {product.quantity} шт.")

    # резервируем
    product.quantity -= schemas.quantity
    cart_item = CartItem(
        product_id=schemas.product_id,
        quantity=schemas.quantity,
        user_id=user.id,
        reserved_until=datetime.utcnow() + timedelta(minutes=15)
    )
    session.add(product)
    session.add(cart_item)
    await session.commit()
    await session.refresh(cart_item)
    return cart_item



async def remove_from_cart(session: AsyncSession, cart_item_id: int, current_user: User = Depends(get_current_user)):
    # 1. Поиск товара в карзине
    query = select(CartItem).where(
        CartItem.id == cart_item_id,
        CartItem.user_id == current_user.id
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


async def changes_quantity_cart(session: AsyncSession,
                                quantity_id: int,
                                new_quantity: int,
                                current_user: User = Depends(get_current_user)):
    # 1. Поиск товара в карзине
    query = select(CartItem).where(
        CartItem.id == quantity_id,
        CartItem.user_id == current_user.id
    )
    result = await session.execute(query)
    cart_item = result.scalars().first()

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар в корзине не найден"
        )

    product = await session.get(Product, cart_item.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден или недоступен"
        )


    #  Если новое количество больше, чем в корзине — зарезервировать доп. товары
    if new_quantity > cart_item.quantity:
        diff = new_quantity - cart_item.quantity
        if product.quantity < diff:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"На складе осталось только {product.quantity} шт."
            )
        product.quantity -= diff # резервируется

    # Если количество уменьшилось - вернуть на склад

    elif new_quantity < cart_item.quantity:
        diff = cart_item.quantity - new_quantity
        product.quantity += diff


    cart_item.quantity = new_quantity
    session.add_all([cart_item,product])
    await session.commit()
    await session.refresh(cart_item)

    return {"detail": "Количество товара обновлено", "cart_item": cart_item}







async def clear_expired_reservations(session: AsyncSession):
    '''
    Очистка просроченных резервов
    :param session:
    :return:
    '''
    query = select(CartItem).where(CartItem.reserved_until < datetime.utcnow())
    result = await session.execute(query)
    expired_items = result.scalars().all()

    for item in expired_items:
        product = await session.get(Product, item.product_id)
        if product:
            product.quantity += item.quantity
            session.add(product)
        await session.delete(item)

    await session.commit()