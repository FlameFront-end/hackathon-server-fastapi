from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    username: str
    password: str

class LoginResponse(BaseModel):
    email: EmailStr
    username: str

