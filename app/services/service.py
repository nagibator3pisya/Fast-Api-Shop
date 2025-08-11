from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from app.api.auth import get_current_user
from app.model.models import Product, Category, CartItem, User, Order, OrderStatus, OrderItems
from app.schemas.CartItem import CartItemCreate


async def all_product(session: AsyncSession):
    result = await session.execute(select(Product))
    return result.scalars().all()


async def all_category(session: AsyncSession):
    result = await session.execute(select(Category))
    return result.scalars().all()


# Корзина


async def my_cart_all(session: AsyncSession, current_user: User = Depends(get_current_user())):
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
        product.quantity -= diff  # резервируется

    # Если количество уменьшилось - вернуть на склад

    elif new_quantity < cart_item.quantity:
        diff = cart_item.quantity - new_quantity
        product.quantity += diff

    cart_item.quantity = new_quantity
    session.add_all([cart_item, product])
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


async def create_order_from_cart(session: AsyncSession, current_user: User = Depends(get_current_user)):
    # # Получил карзиру пользователя
    # query = select(CartItem).where(CartItem.user_id == current_user.id)
    # result = await session.execute(query)
    # cart_items = result.scalars().all()
    # if not cart_items:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Ваша корзина пуста"
    #     )
    #
    # # проверка товара
    # for i in cart_items:
    #     produc = await session.get(Product, i.product_id)
    #     if not produc:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f"{produc.name if produc else i.product_id} недоступен"
    #         )
    #     if produc.quantity < 0:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail=f"Товар {produc.name} отсутствует на складе"
    #         )
    #
    # # Заказ
    #
    # order = Order(
    #     user_id=current_user.id,
    #     status=OrderStatus.NEW,
    #     created_at=datetime.utcnow(),
    #     updated_at=datetime.utcnow()
    # )
    #
    # session.add(order)
    # await session.flush() # order.id
    #
    # # добавление позиции заказа
    #
    # for item in cart_items:
    #     product = await session.get(Product, item.product_id)
    #     order_item = OrderItems(
    #         order_id=order.id,
    #         product_id=product.id,
    #         quantity=item.quantity,
    #         price_at_order=product.price
    #     )
    #     session.add(order_item)
    #     # списываем товар со склада (если не делали резерв заранее)
    #     product.quantity -= item.quantity
    #
    # # 5. Очищаем корзину
    # for item in cart_items:
    #     await session.delete(item)
    #
    # await session.commit()
    #
    # return {
    #     "order_id": order.id,
    #     "status": order.status,
    #     "items": [
    #         {
    #             "product_id": i.product_id,
    #             "quantity": i.quantity,
    #             "price_at_order": i.price_at_order
    #         } for i in order.order_items
    #     ]
    # }
    # 1. Получаем корзину пользователя
    result = await session.execute(
        select(CartItem).options(selectinload(CartItem.product))
        .where(CartItem.user_id == current_user.id)
    )
    cart_items = result.scalars().all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Корзина пуста")

    # 2. Создаём заказ
    order = Order(user_id=current_user.id, status=OrderStatus.NEW)
    session.add(order)
    await session.flush()  # чтобы получить order.id

    # 3. Переносим товары в заказ
    order_items_response = []
    for cart_item in cart_items:
        product = cart_item.product

        if product.quantity < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Товара '{product.name}' недостаточно на складе"
            )

        # Списываем товар со склада
        product.quantity -= cart_item.quantity

        # Добавляем в order_items
        order_item = OrderItems(
            order_id=order.id,
            product_id=product.id,
            quantity=cart_item.quantity,
            price_at_order=product.price
        )
        session.add(order_item)

        # Формируем JSON-ответ для этого товара
        order_items_response.append({
            "product_id": product.id,
            "name": product.name,
            "quantity": cart_item.quantity,
            "price": product.price
        })

        # Удаляем товар из корзины
        await session.delete(cart_item)

    await session.commit()

    # 4. Возвращаем заказ с товарами
    return {
        "order_id": order.id,
        "status": order.status,
        "created_at": order.created_at,
        "items": order_items_response
    }

