from fastapi import APIRouter, Query
from sqlmodel import Session, select
from app.models import UserPublic, UserCreate, Account_User
from app.core.db import SessionDep
from app.utils import hash_password
from typing import Annotated

router = APIRouter()

@router.post("/login")
async def login():
    return {"username": "fakecurrentuser"}

@router.post("/signup", response_model=UserPublic)
async def signup(user: UserCreate, session: SessionDep):
    hashed_password = hash_password(user.password)
    extra_data = {"password": hashed_password, "role": "hacker", "is_active": False}
    db_user = Account_User.model_validate(user, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.put("/verify")
async def verify():
    return {"username": "fakecurrentuser"}

@router.get("/reset_password")
async def reset_password():
    return {"username": "fakecurrentuser"}

@router.post("/refresh")
async def refresh():
    return {"username": "fakecurrentuser"}