from fastapi import APIRouter, Query
from sqlmodel import Session, select
from app.models import User
from app.core.db import SessionDep
from typing import Annotated

router = APIRouter()

@router.post("/login")
async def login():
    return {"username": "fakecurrentuser"}

@router.post("/signup")
async def signup(user: User, session: SessionDep):
    session.add(user)
    session.commit()
    session.refresh(user)
    return session

@router.put("/verify")
async def verify():
    return {"username": "fakecurrentuser"}

@router.get("/reset_password")
async def reset_password():
    return {"username": "fakecurrentuser"}

@router.post("/refresh")
async def refresh():
    return {"username": "fakecurrentuser"}