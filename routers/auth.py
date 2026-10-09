from fastapi import APIRouter, HTTPException, Depends
from schemas import UserSignup, Login, Token
from database import db
from utils.security import create_access_token, get_current_user, verify_password, hash_password
    
router = APIRouter()

@router.post("/signup")
async def signup(user: UserSignup):
    existing = await db.user.find_unique(where={'email': user.email})
    if existing:
        raise HTTPException(status_code=400, detail='email already registered')
    hash = hash_password(user.password)
    new_user = await db.user.create(data={'email': user.email, 'password': hash})
    return{
        'message': 'User Created Successfully',
        'data': {'id': new_user.id, 'email': new_user.email}
    }
    
@router.post("/login")
async def login(user: Login):
    existing = await db.user.find_unique(where={'email': user.email})
    if not existing:
        raise HTTPException(status_code=400, detail='Invalid Credentials')

    password_correct = verify_password(user.password, existing.password)
    if not password_correct:
        raise HTTPException(status_code=400, detail='Invalid Credentials')
    
    token = create_access_token({"sub": str(existing.id)})
    return{
        "access_token": token,
        "token_type": "bearer"
    }
    
@router.get("/me")
async def read_current_User(user_id=Depends(get_current_user)):
    user = await db.user.find_unique(where={"id": user_id})
    return {
        "data": {"id": user.id, "email": user.email}
        }
