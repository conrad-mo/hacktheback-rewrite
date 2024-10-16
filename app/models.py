from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


class UserBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str = Field(index=True)
    role: str
    is_active: bool

class Account_User(UserBase, table=True):
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)    
    password: str = Field()

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    uid: uuid.UUID

class UserUpdate(SQLModel):
    password: str | None = None