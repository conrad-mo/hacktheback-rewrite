from sqlmodel import SQLModel, Field
from typing import Optional
import uuid

class User(SQLModel, table=True):
    password: str = Field()
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str = Field(index=True)
    role: str
    is_active: bool