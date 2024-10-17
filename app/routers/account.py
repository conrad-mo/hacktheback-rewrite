from fastapi import Depends, APIRouter, Query, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.models import UserPublic, UserCreate, Account_User, UserLogin
from app.core.db import SessionDep
from app.utils import hash_password, password_verfiy
from typing import Annotated

router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Uses type application/x-www-form-urlencoded body, not JSON
@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    statement= select(Account_User).where(Account_User.email == form_data.username)
    selected_user = session.exec(statement).first()
    if not selected_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User does not exist"
        )
    if not password_verfiy(form_data.password, selected_user.password):
      raise HTTPException(
            status_code=status.HTTP_401_NOT_FOUND, 
            detail="Password is incorrect"
        )
    return {"access_token": selected_user.email, "token_type": "bearer"}

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

@router.get("/reset_password")
async def reset_password():
    return {"username": "fakecurrentuser"}

@router.post("/refresh")
async def refresh():
    return {"username": "fakecurrentuser"}