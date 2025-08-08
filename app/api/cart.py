from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.deps.dependes import get_db
from app.model.models import User
from app.schemas.CartItem import CartItemOut, CartItemCreate
from app.services import service

cart_router = APIRouter(prefix="/cart", tags=["cart"])


@cart_router.get('/my_cart', response_model=list[CartItemOut])
async def my_cart(session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await service.my_cart_all(session=session, current_user=current_user)
    if result is None:
        return []
    return result


@cart_router.post('/add_to_cart', response_model=CartItemOut)
async def add_cart(schemas_app: CartItemCreate, session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await service.add_to_cart(session=session, schemas=schemas_app, user=current_user)
    return result


# @cart_router.put('/change_quantity/')
# async def change_quantity_cart(quantity_id: int):
#     ...
#
#
# @cart_router.delete('/delete_product/')
# async def delete_to_product_cart(product_id: int):
#     ...
#
#
# @cart_router.post('/checkout/')
# async def product_checkout():
#     ...