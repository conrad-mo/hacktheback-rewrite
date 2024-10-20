from typing import Annotated

from fastapi import APIRouter, Depends
from app.core.db import SessionDep
from app.models.user import Account_User
from app.routers.account import get_current_user
from app.models.forms import Forms_Application, Forms_HackathonApplicant, StatusEnum
from sqlmodel import select
from datetime import datetime, timezone

router = APIRouter()


async def createapplication(current_user: Account_User, session: SessionDep):
    application = Forms_Application(
        uid=current_user.uid,
        is_draft=False,
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
