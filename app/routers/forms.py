from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import select

from app.core.db import SessionDep
from app.models.forms import (
    Forms_Application,
    Forms_HackathonApplicant,
    Forms_Question,
    StatusEnum,
)
from app.models.user import Account_User
from app.routers.account import get_current_user

router = APIRouter()


@router.post("/createapplication")
async def createapplication(
    current_user: Annotated[Account_User, Depends(get_current_user)],
    session: SessionDep,
):
    application = Forms_Application(
        uid=current_user.uid,
        is_draft=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db_application = Forms_Application.model_validate(application)
    hackathon_applicant = Forms_HackathonApplicant(
        application_id=db_application.application_id, status=StatusEnum.APPLYING
    )
    db_hackathon_applicant = Forms_HackathonApplicant.model_validate(
        hackathon_applicant
    )
    session.add(db_application)
    session.add(db_hackathon_applicant)
    session.commit()
    session.refresh(db_application)
    session.refresh(db_hackathon_applicant)
    return db_application


@router.get("/getquestions")
async def getquestions(session: SessionDep) -> list[Forms_Question]:
    statement = select(Forms_Question)
    return session.exect(statement).first()


@router.get("/getapplication", response_model=Forms_Application)
async def getapplication(
    current_user: Annotated[Account_User, Depends(get_current_user)],
    session: SessionDep,
):
    statement = select(Forms_Application).where(
        Forms_Application.uid == current_user.uid
    )
    application = session.exec(statement).first()
    if application is None:
        application = await createapplication(current_user, session)
    return application


@router.post("/save")
async def save():
    return {"username": "fakecurrentuser"}


@router.post("/submit")
async def submit():
    return {"username": "fakecurrentuser"}
