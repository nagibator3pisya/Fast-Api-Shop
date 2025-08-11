from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from app.api.auth import get_current_user
from app.deps.dependes import get_db
from app.model.models import User
from app.schemas.CartItem import CartItemOut, CartItemCreate
from app.services import service
from app.services.service import remove_from_cart, changes_quantity_cart, create_order_from_cart

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



@cart_router.delete("/remove_from_cart/{cart_item_id}")
async def delete_cart(cart_item_id: int, session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await remove_from_cart(session=session, cart_item_id=cart_item_id, current_user=current_user)



@cart_router.put('/change_quantity/{cart_item_id}/')
async def change_quantity_cart(quantity_id: int,
                               new_quantity: int,
                               current_user: User = Depends(get_current_user),
                               session: AsyncSession = Depends(get_db)):
    return await changes_quantity_cart(session=session, quantity_id=quantity_id,
                                       new_quantity=new_quantity, current_user=current_user)



@cart_router.post('/checkout/')
async def product_checkout(session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await create_order_from_cart(session=session, current_user=current_user)