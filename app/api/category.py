from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.dependes import get_db
from app.services.service import all_category

category_router = APIRouter(prefix="/category", tags=["category"])


@category_router.get('/all/')
async def category_all(session: AsyncSession = Depends(get_db)):
    category = await all_category(session=session)
    if category is None:
        raise HTTPException(status_code=404, detail='Нет продуктов')
    return category


