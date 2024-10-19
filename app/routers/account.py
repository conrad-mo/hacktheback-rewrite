import os
from datetime import timedelta
from typing import Annotated

import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from sqlmodel import select

from app.core.db import SessionDep
from app.models.token import Token, TokenData
from app.models.user import Account_User, UserCreate, UserPublic
from app.utils import create_access_token, hash_password, password_verfiy

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={
        "admin": "Allow user to call admin routes",
        "volunteer": "Allow user to call qr routes",
    },
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials or expired token",
    headers={"WWW-Authenticate": "Bearer"},
)


async def decode_jwt(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        scopes: list[str] = payload.get("scopes", [])
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, scopes=scopes)
    except InvalidTokenError:
        raise credentials_exception
    return token_data


async def get_current_user(
    token_data: Annotated[TokenData, Depends(decode_jwt)], session: SessionDep
):
    statement = select(Account_User).where(Account_User.email == token_data.email)
    user = session.exec(statement).first()
    if user is None:
        raise credentials_exception
    return user


# Uses type application/x-www-form-urlencoded for response body, not JSON
@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:
    statement = select(Account_User).where(Account_User.email == form_data.username)
    selected_user = session.exec(statement).first()
    if not selected_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    if not password_verfiy(form_data.password, selected_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_NOT_FOUND, detail="Password is incorrect"
        )
    if not selected_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not activated"
        )
    scopes = []
    if selected_user.role == "admin":
        scopes.append("admin")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(selected_user.email), "scopes": scopes},
        SECRET_KEY=SECRET_KEY,
        ALGORITHM=ALGORITHM,
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/signup", response_model=UserPublic)
async def signup(user: UserCreate, session: SessionDep):
    statement = select(Account_User).where(Account_User.email == user.email)
    selected_user = session.exec(statement).first()
    if selected_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email already in use"
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


@router.post("/activate")
async def activate():
    return {"username": "fakecurrentuser"}


@router.post("/refresh")
async def refresh(token_data: Annotated[TokenData, Depends(decode_jwt)]) -> Token:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(token_data.email), "scopes": token_data.scopes},
        SECRET_KEY=SECRET_KEY,
        ALGORITHM=ALGORITHM,
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
