from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: EmailStr    


class UserCreate(UserBase):
    password: str
    repeat_password: str
    role: int = 1 # 1-invitado, 2-admin


class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None  # si viene, se hashea
    repeat_password: Optional[str] = None
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    disabled: bool

    class Config:
        from_attributes = True  # convierte modelos SQLAlchemy → Pydantic