from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel import select

from app.core.db import SessionDep
from app.models.forms import ApplicationResponse, Forms_Question
from app.models.user import Account_User
from app.utils import createapplication, get_current_user

router = APIRouter()


@router.get("/getquestions")
async def getquestions(session: SessionDep) -> list[Forms_Question]:
    statement = select(Forms_Question)
    return session.exec(statement)


@router.get("/getapplication", response_model=ApplicationResponse)
async def getapplication(
    current_user: Annotated[Account_User, Depends(get_current_user)],
    session: SessionDep,
):
    application = current_user.application
    if application is None:
        application = await createapplication(current_user, session)
    return {
        "application": application,
        "form_answers": application.form_answers,
        "form_answersfile": application.form_answersfile.original_filename,
    }


@router.post("/save")
async def save(
    question_id: str,
    answer: str,
    current_user: Annotated[Account_User, Depends(get_current_user)],
    session: SessionDep,
):
    return {"username": "fakecurrentuser"}


@router.post("/uploadresume")
async def uploadresume(
    file: UploadFile,
    current_user: Annotated[Account_User, Depends(get_current_user)],
    session: SessionDep,
):
    if file.filename.endswith(".pdf"):
        file_data = await file.read()
        current_user.application.form_answersfile.original_filename = file.filename
        current_user.application.form_answersfile.file = file_data
        current_user.application.updated_at = datetime.now(timezone.utc)
        session.add(current_user.application.form_answersfile)
        session.add(current_user.application)
        session.commit()
        session.refresh(current_user.application.form_answersfile)
        session.refresh(current_user.application)
        return current_user.application.form_answersfile.original_filename
    else:
        raise HTTPException(status_code=404, detail="File not pdf")


@router.post("/submit")
async def submit():
    return {"username": "fakecurrentuser"}
