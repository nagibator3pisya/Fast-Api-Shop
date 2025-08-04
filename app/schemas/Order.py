from enum import Enum

from pydantic import BaseModel
from typing import List
from datetime import datetime


class Status_Enum(str,Enum):
    NEW = "new"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"
    FAILED = "failed"



class OrderBase(BaseModel):
    status: Status_Enum

class OrderCreate(BaseModel):
    # можно будет указать адрес, если добавишь
    pass  # создаётся из корзины

class OrderOut(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
