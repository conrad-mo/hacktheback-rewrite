from sqlmodel import SQLModel, Field
from pydantic import BaseModel
import uuid

class UserBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str = Field(index=True)

class UserLogin(BaseModel):
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