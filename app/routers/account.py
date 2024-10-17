from datetime import datetime, timedelta, timezone

from fastapi import Depends, APIRouter, Query, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.models import UserPublic, UserCreate, Account_User, UserLogin, Token, TokenData
from app.core.db import SessionDep
from app.utils import hash_password, password_verfiy
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError


SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    statement= select(Account_User).where(Account_User.email == token_data.email)
    user = session.exec(statement).first()
    if user is None:
        raise credentials_exception
    return user

#Uses type application/x-www-form-urlencoded body, not JSON
@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> Token:
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
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": selected_user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

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

@router.get("/me", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[Account_User, Depends(get_current_user)],
):
    return current_user

@router.get("/reset_password")
async def reset_password():
    return {"username": "fakecurrentuser"}

@router.post("/refresh")
async def refresh():
    return {"username": "fakecurrentuser"}