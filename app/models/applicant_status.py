from sqlmodel import SQLModel, Field
from pydantic import BaseModel
import uuid

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

class Applicant_Status(SQLModel, table=True):
    uid: uuid.UUID = Field(index=True, primary_key=True)    
    status: StatusEnum = Field()