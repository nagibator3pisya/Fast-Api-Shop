from datetime import datetime
from enum import Enum
from itertools import product
from typing import List

from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from sqlalchemy import Enum as SQLEnum



class OrderStatus(str, Enum):
    NEW = "new"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"
    FAILED = "failed"




class User(Base):
    __tablename__ = 'user'
    name: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    email: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    cart_items = relationship('CartItem',back_populates='user')


class Category(Base):
    """
    passive_deletes=True
    SQLAlchemy не будет загружать дочерние объекты, а просто доверит каскад базе
    """
    __tablename__ = 'category'
    name: Mapped[str] = mapped_column(String,nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    products: Mapped[List["Product"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",  # каскад на уровне ORM
        passive_deletes=True
    )


class Product(Base):
    __tablename__ = 'product'
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer,nullable=False)
    quantity: Mapped[int] = mapped_column(Integer,nullable=False, default=1) # количество
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id", ondelete="CASCADE"),  # каскадное удаление
        nullable=False
    )

    category: Mapped["Category"] = relationship(back_populates="products")

    cart_items = relationship('CartItem', back_populates='product')


class CartItem(Base):
    # карзина пользователя, расширить карзину

    __tablename__ = 'cartitem'
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    reserved_until: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    product = relationship("Product", back_populates="cart_items")
    user = relationship("User", back_populates="cart_items")




class Order(Base):
    __tablename__ = 'order'
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus),
        default=OrderStatus.NEW
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    order_items = relationship("OrderItems", back_populates="order", cascade="all, delete-orphan")

class OrderItems(Base):
    __tablename__ = 'orderitem'
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer)
    price_at_order: Mapped[int] = mapped_column(Integer)
    order = relationship("Order", back_populates="order_items")





















