from pydantic import BaseModel, EmailStr
from typing import Optional



class UserBase(BaseModel):
    name: Optional[str]
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(BaseModel):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

        