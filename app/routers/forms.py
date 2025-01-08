from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from sqlmodel import select

from app.core.db import SessionDep
from app.models.forms import (
    Forms_Application,
    Forms_Question,
)
from app.models.user import Account_User
from app.utils import createapplication, get_current_user

router = APIRouter()


@router.get("/getquestions")
async def getquestions(session: SessionDep) -> list[Forms_Question]:
    statement = select(Forms_Question)
    return session.exec(statement)


@router.get("/getapplication", response_model=Forms_Application)
async def getapplication(
    current_user: Annotated[Account_User, Depends(get_current_user)],
    session: SessionDep,
):
    application = current_user.application
    if application is None:
        application = await createapplication(current_user, session)
    return application


@router.post("/save")
async def save(
    session: SessionDep,
):
    return {"username": "fakecurrentuser"}


@router.post("/uploadresume")
async def uploadresume(
    file: UploadFile,
    current_user: Annotated[Account_User, Depends(get_current_user)],
    session: SessionDep,
):
    file_data = await file.read()
    return {"username": "fakecurrentuser"}


@router.post("/submit")
async def submit():
    return {"username": "fakecurrentuser"}
