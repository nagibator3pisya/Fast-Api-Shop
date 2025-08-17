import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.admin import admin_router
from app.api.autg_log import aut_log
from app.api.cart import cart_router
from app.api.category import category_router
from app.api.product import product_router

app = FastAPI()




app.include_router(admin_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(cart_router)
app.include_router(aut_log)





if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)