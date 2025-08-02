from sqlalchemy.ext.asyncio import AsyncSession

from app.model.models import Category
from app.schemas.Category_Scemas import CategoryCreate


async def add_category(schemas_add:CategoryCreate,session:AsyncSession):
    result = Category(**schemas_add.model_dump())
    session.add(result)
    await session.commit()
    await session.refresh(result)
    return result
