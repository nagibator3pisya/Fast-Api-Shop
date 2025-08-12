from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from app.deps.dependes import get_db
from app.schemas.Category import CategoryCreate, CategoryUpdate
from app.schemas.Product import ProductCreate, ProductUpdate
from app.services import service_admins

admin_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_router.post('/add_categories/')
async def add_categories(add_categories: CategoryCreate, session: AsyncSession = Depends(get_db)):
    return await service_admins.add_category(schemas_add=add_categories,session=session)


@admin_router.put('/update_categories/{id_category}/')
async def update_categories(id_category: int, categoryes: CategoryUpdate, session: AsyncSession = Depends(get_db)):
    update = await service_admins.update_categories(category_id=id_category, category_data=categoryes, session=session)
    if update is None:
        raise HTTPException(status_code=404, detail='Такой категории нет')
    return update


@admin_router.post('/add_products/')
async def add_products(product_schemas: ProductCreate, session: AsyncSession = Depends(get_db)):
    return await service_admins.add_products(schemas_add=product_schemas, session=session)


@admin_router.put('/update_products/{id_products}/')
async def update_products(id_products: int, product_schemas: ProductUpdate, session: AsyncSession = Depends(get_db)):
    update = await service_admins.update_products(products_id=id_products, session=session,
                                                  product_data=product_schemas)
    if update is None:
        raise HTTPException(status_code=404, detail='Такого продукта нет')
    return update


@admin_router.delete('/delete_category/{id_category}')
async def delete_category(id_category: int, session: AsyncSession = Depends(get_db)):
   delete = await service_admins.delete_category(category_id=id_category, session=session)
   return delete


@admin_router.delete('/delete_product/{id_product}')
async def delete_product(id_product: int, session: AsyncSession = Depends(get_db)):
   delete = await service_admins.delete_product(product_id=id_product, session=session)
   return delete



@admin_router.post('/restock_product/{product_id}/')
async def restock_products(id_product: int, quantity: int,session:AsyncSession = Depends(get_db)):
    restock = await service_admins.restock_product(session=session, product_id=id_product, quantity=quantity)
    return restock

