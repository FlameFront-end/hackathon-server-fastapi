from datetime import datetime
from passlib.hash import sha256_crypt, pbkdf2_sha256

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


def login(session: SessionType, email) -> User:
    user_query = session.query(User).filter_by(email=email).one()
    if not user_query:
        raise ValueError("Пользователь с таким email не найден.")
    return user_query

def hash_password(password):
    return sha256_crypt.hash(password)

def verify_pass(user_pass, hashed_pass):
    if sha256_crypt.verify(user_pass, hashed_pass):
        return True
    else:
        return False
