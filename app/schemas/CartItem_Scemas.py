from pydantic import BaseModel


class CartItemBase(BaseModel):
    product_id: int
    quantity: int


class CartItemCreate(CartItemBase):
    pass


class CartItemOut(CartItemBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
