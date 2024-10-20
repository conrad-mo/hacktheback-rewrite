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


class Forms_Response(SQLModel, table=True):
    uid: str = Field(primary_key=True)
    is_draft: bool
    created_at: timezone
    updated_at: timezone
    application_id: str = Field(default_factory=uuid.uuid4, index=True)


class FormResponseUpdate(SQLModel):
    idk: str | None = None


# Separate bc no race conditions?
class Forms_HackathonApplicant(SQLModel, table=True):
    application_id: uuid.UUID = Field(primary_key=True)
    status: StatusEnum = Field()


class Update_Forms_HackathonApplicant(SQLModel):
    uid: uuid.UUID
    status: StatusEnum


class Forms_Question(SQLModel, table=True):
    order: int


# Python enums
# user_status = StatusEnum.APPLYING

# if user_status == StatusEnum.ACCEPTED:
#     print("User has been accepted.")
