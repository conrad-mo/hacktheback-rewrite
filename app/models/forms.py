import uuid
from datetime import timezone
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
    WALK_IN_SUBMITTED = "WALK_IN_SUBMITTED"


class Forms_Application(SQLModel, table=True):
    uid: uuid.UUID = Field(primary_key=True)
    is_draft: bool
    created_at: timezone
    updated_at: timezone
    application_id: uuid.UUID = Field(default_factory=uuid.uuid4, index=True)


class Forms_ApplicationUpdate(SQLModel):
    is_draft: bool | None = None
    updated_at: timezone | None = None


# Separate bc no race conditions when updating rows?
class Forms_HackathonApplicant(SQLModel, table=True):
    application_id: uuid.UUID = Field(primary_key=True)
    status: StatusEnum = Field()


class Forms_HackathonApplicantUpdate(SQLModel):
    status: StatusEnum | None = None


class Forms_Question(SQLModel, table=True):
    question_id: uuid.UUID = Field(default_factory=uuid.uuid4, index=True)
    order: int = Field(index=True)
    label: str
    required: bool


class Forms_Answer(SQLModel, table=True):
    application_id: uuid.UUID = Field(primary_key=True)
    question_id: uuid.UUID = Field(index=True)
    answer: str


class Forms_AnswerUpdate(SQLModel):
    answer: str | None = None


# Python enums
# user_status = StatusEnum.APPLYING

# if user_status == StatusEnum.ACCEPTED:
#     print("User has been accepted.")
