from typing import Optional

from pydantic import BaseModel



class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    quantity: int
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    descriptions: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None


class ProductOut(ProductBase):
    """
        {
          "id": 1,
          "name": "Ноутбук",
          "description": "Мощный ноутбук с SSD",
          "price": 75000,
          "quantity": 4,
          "category_id": 2,
          "is_active": true
        }
    """
    id: int
    is_active: bool


    class Config:
        from_attributes = True




