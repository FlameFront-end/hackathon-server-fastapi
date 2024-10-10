from typing import Optional
from pydantic import BaseModel, EmailStr, SecretStr
from jwt import encode, decode


class JWTPayload(BaseModel):
    sub: str
    iat: int
    exp: int


class JWTToken(BaseModel):
    access_token: str
    refresh_token: Optional[str]

class UserBase(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    username: str
    password: str
    token: Optional[str] = None

class LoginResponse(BaseModel):
    token: JWTToken

class RegisterResponse(BaseModel):
    token: JWTToken