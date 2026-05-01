from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    nim_nip: str
    full_name: str
    email: EmailStr
    password: str
    role: Optional[str] = "mahasiswa"


class UserLogin(BaseModel):
    nim_nip: str
    password: str


class UserOut(BaseModel):
    id: int
    nim_nip: str
    full_name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut
