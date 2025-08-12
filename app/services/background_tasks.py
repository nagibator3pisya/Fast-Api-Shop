import asyncio

from app.core.config import async_session_maker
from app.main import app
from app.services.service import clear_expired_reservations


@app.on_event("startup")
async def start_cleanup_task():
    async def cleaner():
        while True:
            async for session in async_session_maker():
                await clear_expired_reservations(session)
            await asyncio.sleep(60)  # проверка каждые 60 секунд
    asyncio.create_task(cleaner())