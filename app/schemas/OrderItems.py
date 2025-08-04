from pydantic import BaseModel


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price_at_order : int


class OrderItemOut(OrderItemBase):
    id: int
    order_id: int


    class Config:
        from_attributes = True
