from fastapi import APIRouter, Query
from sqlmodel import Session, select
from app.models import UserPublic, UserCreate, Account_User, UserLogin
from app.core.db import SessionDep
from app.utils import hash_password, password_verfiy
from typing import Annotated

router = APIRouter()

@router.post("/login")
async def login(user: UserLogin, session: SessionDep) -> bool:
    statement= select(Account_User).where(Account_User.email == user.email)
    selected_user = session.exec(statement).first()
    if not selected_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User does not exist"
        )
    return password_verfiy(user.password, selected_user.password)

@router.post("/signup", response_model=UserPublic)
async def signup(user: UserCreate, session: SessionDep):
    statement= select(Account_User).where(Account_User.email == user.email)
    selected_user = session.exec(statement).first()
    if selected_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Email already in use"
        )
    hashed_password = hash_password(user.password)
    extra_data = {"password": hashed_password, "role": "hacker", "is_active": False}
    db_user = Account_User.model_validate(user, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.put("/token")
async def verify():
    return {"username": "fakecurrentuser"}

@router.get("/reset_password")
async def reset_password():
    return {"username": "fakecurrentuser"}

@router.post("/refresh")
async def refresh():
    return {"username": "fakecurrentuser"}