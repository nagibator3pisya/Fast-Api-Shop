import uvicorn
from fastapi import FastAPI

from app.api.admin import admin_router
from app.api.category import category_router
from app.api.product import product_router

app = FastAPI()



# app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(products.router, prefix="/products", tags=["products"])
# app.include_router(cart.router, prefix="/cart", tags=["cart"])
# app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(admin_router)
app.include_router(product_router)
app.include_router(category_router)





if __name__ == '__main__':
    uvicorn.run('main:app',reload=True)