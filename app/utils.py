import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import select

from app.core.db import SessionDep
from app.models.token import TokenData
from app.models.user import Account_User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

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
        fullName: str = payload.get("fullName")
        firstName: str = payload.get("firstName")
        lastName: str = payload.get("lastName")
        if email is None:
            raise credentials_exception
        token_data = TokenData(
            email=email,
            fullName=fullName,
            firstName=firstName,
            lastName=lastName,
            scopes=scopes,
        )
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


def create_access_token(
    data: dict, SECRET_KEY: str, ALGORITHM: str, expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=1)
    to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
