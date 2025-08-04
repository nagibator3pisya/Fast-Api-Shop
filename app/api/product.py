from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.dependes import get_db
from app.services.service import all_product

product_router = APIRouter(prefix="/products", tags=["products"])


@product_router.get('/all/')
async def product_all(session: AsyncSession = Depends(get_db)):
    product = await all_product(session=session)
    if product is None:
        raise HTTPException(status_code=404, detail='Нет продуктов')
    return product


