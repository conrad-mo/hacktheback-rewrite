import uuid
from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class StatusEnum(str, Enum):
    APPLYING = "APPLYING"
    APPLIED = "APPLIED"
    UNDER_REVIEW = "UNDER_REVIEW"
    WAITLISTED = "WAITLISTED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    ACCEPTED_INVITE = "ACCEPTED_INVITE"
    REJECTED_INVITE = "REJECTED_INVITE"
    SCANNED_IN = "SCANNED_IN"
    WALK_IN = "WALK_IN"
    WALK_IN_SUBMITTED = "WALK_IN SUBMITTED"


class Forms_Application(SQLModel, table=True):
    uid: uuid.UUID = Field(primary_key=True)
    is_draft: bool
    created_at: datetime
    updated_at: datetime
    application_id: uuid.UUID = Field(default_factory=uuid.uuid4, index=True)


class Forms_ApplicationUpdate(SQLModel):
    is_draft: bool | None = None
    updated_at: datetime | None = None


# Separate bc no race conditions when updating rows?
class Forms_HackathonApplicant(SQLModel, table=True):
    application_id: uuid.UUID = Field(primary_key=True)
    status: StatusEnum = Field()


class Forms_HackathonApplicantUpdate(SQLModel):
    status: StatusEnum | None = None


# Future reference: Designed it like this to prevent people from directly submitting answers to invalid questions
class Forms_Question(SQLModel, table=True):
    question_id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True
    )  # Wait do we even need this field?
    order: int = Field(index=True)  # Wait do we even need this field?
    label: str = Field(index=True)
    required: bool  # Wait do we even need this field?


# API to return everything related and we just pass id to modify form answers or else need to index question table for every update
class Forms_Answer(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    application_id: uuid.UUID = Field(index=True)
    question_id: uuid.UUID = Field(index=True)
    answer: str


class Forms_AnswerUpdate(SQLModel):
    answer: str | None = None
