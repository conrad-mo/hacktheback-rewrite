from fastapi import APIRouter, Query
from sqlmodel import Session, select
from app.models import User
from app.core.db import SessionDep
from typing import Annotated

router = APIRouter()

@router.get("/getusers")
def get_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users