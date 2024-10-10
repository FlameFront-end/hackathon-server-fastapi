from datetime import datetime

from dns.dnssecalgs import algorithms
from dns.dnssectypes import Algorithm
from passlib.hash import sha256_crypt, pbkdf2_sha256

import time
import jwt
from fastapi import Request
from .schemas import JWTPayload, JWTToken
import secrets


from sqlalchemy import (
    create_engine
)

from sqlalchemy.orm import (
    Session as SessionType,
    sessionmaker,
    scoped_session,
)

from .models import User
from .schemas import UserBase

SECRET_KEY = secrets.token_bytes(64)

DB_URL = "postgresql://admin:root@localhost:5432/users"
DB_ECHO = False
engine = create_engine(url=DB_URL, echo=DB_ECHO)


def init_db():
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    session: SessionType = Session()
    return session


def query_all_users(session: SessionType) -> list[UserBase]:
    users = session.query(User).all()
    return users

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, secret: str):
    to_encode = data.copy()
    expire = time.time() + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, secret: str):
    try:
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def generate_access_token(user):
    data = {
        "sub": user.email,
        "iat": int(time.time()),
        "exp": int(time.time()) + ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }
    access_token = create_access_token(data, SECRET_KEY)
    return access_token

def hash_password(password):
    return sha256_crypt.hash(password)

def verify_pass(user_pass, hashed_pass):
    if sha256_crypt.verify(user_pass, hashed_pass):
        return True
    else:
        return False
