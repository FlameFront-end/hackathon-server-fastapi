from fastapi import APIRouter
from pydantic import EmailStr

from . import crud
from .crud import init_db, hash_password
from .schemas import UserBase, LoginResponse, JWTToken
from .models import User

SESSION = init_db()
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("")
async def get_users():
    users = crud.query_all_users(SESSION)
    response = {}
    for user in users:
        response[user.id] = user.username
    return response


@router.post("/login")
async def login(email: EmailStr, password: str):
    user_query = SESSION.query(User).filter_by(email=email).one()
    if not user_query:
        return {"error": "Invalid email or password"}
    if not crud.verify_pass(password, user_query.password):
        return {"error": "Invalid email or password"}
    return {"token": user_query.token}


@router.post("/register")
async def register(email: EmailStr, username: str, password: str):
    password = hash_password(password)
    user = User(email=email, username=username, password=password)
    access_token = crud.generate_access_token(user)
    user.token = access_token
    SESSION.add(user)
    SESSION.commit()
    return {"token": access_token}
