from fastapi import APIRouter, Query
from sqlmodel import Session, select
from app.models import Item
from app.core.db import SessionDep, create_db_and_tables
from typing import Annotated

router = APIRouter()

@router.post("/login")
async def login():
    return {"username": "fakecurrentuser"}

@router.post("/signup")
async def signup():
    return {"username": "fakecurrentuser"}

@router.put("/verify")
async def verify():
    return {"username": "fakecurrentuser"}

@router.get("/reset_password")
async def reset_password():
    return {"username": "fakecurrentuser"}

@router.post("/refresh")
async def refresh():
    return {"username": "fakecurrentuser"}

@router.post("/items")
async def create_item(item: Item, session: SessionDep):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.get("/items")
def read_items(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Item]:
    items = session.exec(select(Item).offset(offset).limit(limit)).all()
    return items