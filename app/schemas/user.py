from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    usr: str

class UserCreate(UserBase):
    psswrd: str

class UserUpdate(UserBase):
    usr: Optional[str] = None
    psswrd: Optional[str] = None

class UserLogin(BaseModel):
    usr: str
    psswrd: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True