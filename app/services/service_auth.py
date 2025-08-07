from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.models import User
from app.schemas.User import UserCreate


async def search_email(token_data: str, session: AsyncSession):
    stmt = select(User).where(User.email == token_data)
    result = await session.execute(stmt)
    user = result.scalars().first()
    return user


# поиск есть ли такой челове или нет
async def filter_user_to_db(session: AsyncSession, user: UserCreate):
    stmt = select(User).filter(
        or_(
            User.email == user.email,
            User.name == user.name
        )
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_email(session: AsyncSession, email: str):
    result = await session.execute(select(User).filter(User.email == email))
    return result.scalars().first()