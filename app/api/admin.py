from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from app.deps.dependes import get_db
from app.schemas.Category_Scemas import CategoryCreate
from app.services import service_admins

admin_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_router.post('/add_categories/')
async def add_categories(add_categories: CategoryCreate, session: AsyncSession = Depends(get_db)):
   return await service_admins.add_category(schemas_add=add_categories, session=session)


@admin_router.get('/update_categories/{id_category}/')
async def update_categories(id_category):
   ...




@admin_router.get('/add_products/')
async def add_products(id_category):
   ...


@admin_router.get('/update_products/{id_products}/')
async def update_categories(id_products):
   ...



@admin_router.get('/all_orders/')
async def all_orders():
   ...