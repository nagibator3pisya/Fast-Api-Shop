from fastapi import APIRouter

product_router = APIRouter(refix="/products", tags=["products"])


@product_router.get('/all/')
async def product_all():
    ...