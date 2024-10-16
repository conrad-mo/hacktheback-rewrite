from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# Dependency for using the database session
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Initialize the database
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)