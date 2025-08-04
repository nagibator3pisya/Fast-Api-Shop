from pydantic import BaseModel


class CartBase(BaseModel):
    product_id: int
    quantity: int


class CartCreate(CartBase):
    pass


class CartOut(CartBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
