from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import db
from routers import auth
from schemas import Login, UserSignup, Token
from utils.security import create_access_token, get_current_user, hash_password, verify_password

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()
    
app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix='/auth')

@app.get("/")
def read_root():
    return {"message": "Welcome to Habit_tracker Api"}


#atonation is using the @ sysmbol