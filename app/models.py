from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


class UserBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str = Field(index=True)

class UserLogin(SQLModel):
    email: str
    password: str

class Account_User(UserBase, table=True):
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)    
    password: str = Field()
    role: str
    is_active: bool

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    uid: uuid.UUID
    role: str
    is_active: bool

class UserUpdate(SQLModel):
    password: str | None = None

class Form(SQLModel):
    idk: str

class FormUpdate(SQLModel):
    idk: str | None = None