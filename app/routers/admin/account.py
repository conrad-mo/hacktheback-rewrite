from fastapi import APIRouter, Query
from sqlmodel import select
from app.models.user import UserPublic, Account_User
from app.core.db import SessionDep
from typing import Annotated

router = APIRouter()


@router.get("/getusers", response_model=list[UserPublic])
def get_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[UserPublic]:
    users = session.exec(select(Account_User).offset(offset).limit(limit)).all()
    return users
