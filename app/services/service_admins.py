from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.model.models import Category, Product, User
from app.schemas.Category import CategoryCreate, CategoryUpdate
from app.schemas.Product import ProductCreate, ProductUpdate


async def add_category(schemas_add: CategoryCreate, session: AsyncSession):
    result = Category(**schemas_add.model_dump())
    session.add(result)
    await session.commit()
    await session.refresh(result)
    return result


async def update_categories(category_id: int, category_data: CategoryUpdate, session: AsyncSession):
    result = await session.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()

    if not category:
        return None

    for k, v in category_data.model_dump().items():
        setattr(category, k, v)
        await session.commit()
        await session.refresh(category)
        return category



async def add_products(schemas_add: ProductCreate, session: AsyncSession):
    result = Product(**schemas_add.model_dump())
    session.add(result)
    await session.commit()
    await session.refresh(result)
    return result



async def update_products(session: AsyncSession, products_id: int,product_data: ProductUpdate):
    result = await session.execute(select(Product).where(Product.id == products_id))
    category = result.scalar_one_or_none()

    if not category:
        return None

    for k, v in product_data.model_dump().items():
        setattr(category, k, v)
        await session.commit()
        await session.refresh(category)
        return category


async def delete_product(product_id: int,session: AsyncSession):
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        return None

    await session.delete(product)
    await session.commit()
    return {"detail": "Продукт удален"}


async def delete_category(category_id: int,session: AsyncSession):
    result = await session.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")

    await session.delete(category)
    await session.commit()
    return {"message": "Категория и все её продукты удалены"}


async def add_admins(user_id: int, session: AsyncSession):
    # Ищем пользователя
    result = await session.execute(select(User).where(User.id == user_id))
    target_user = result.scalar_one_or_none()


    if not target_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    target_user.is_admin = True
    await session.commit()

    return {"message": f"Пользователь {target_user.email} теперь администратор"}




async def restock_product(session: AsyncSession,
                          product_id: int,
                          quantity: int,
                          ):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail='Количество должно быть больше 0')

    product = await session.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар не найден"
        )

    # увеличение остатка
    product.quantity += quantity

    # Если был не активен и теперь есть остаток - вкл
    if product.quantity > 0:
        product.is_active = True

    await session.commit()

    return {
        'detail': f'Товар "{product.name}" пополнен на {quantity} шт.',
        'new_quantity': product.quantity,
        "is_active": product.is_active
    }


