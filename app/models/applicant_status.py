from sqlmodel import SQLModel, Field
import uuid
from enum import Enum

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

class Applicant_Status(SQLModel, table=True):
    uid: uuid.UUID = Field(index=True, primary_key=True)    
    status: StatusEnum = Field()

class Update_Applicant_Status(SQLModel):
    uid: uuid.UUID  
    status: StatusEnum

#Python enums
# user_status = StatusEnum.APPLYING

# if user_status == StatusEnum.ACCEPTED:
#     print("User has been accepted.")