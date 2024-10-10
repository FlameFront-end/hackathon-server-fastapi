from fastapi import FastAPI
from .auth.crud import query_all_users
from .auth.router import router as auth_router


app = FastAPI(title="Auth App")
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"Start": "App"}