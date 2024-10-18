from sqlmodel import SQLModel, Field

class Forms_HackathonApplicant(SQLModel, table=True):
    uid: str = Field(primary_key=True)
    status: str
    application_id: str = Field(default_factory=uuid.uuid4,index=True)

class FormHackathonApplicantUpdate(SQLModel):
    idk: str | None = None