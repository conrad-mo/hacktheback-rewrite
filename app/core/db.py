import os
from typing import Annotated, List

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine, select

from app.models.forms import Forms_Question

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


def seed_questions(questions: List, session: Session):
    for index, question in enumerate(questions):
        statement = select(Forms_Question).where(
            Forms_Question.label == question["label"]
        )
        selected_question = session.exec(statement).first()
        if not selected_question:
            db_question = Forms_Question.model_validate(
                question, update={"order": index}
            )
            session.add(db_question)
            session.commit()
            session.refresh(db_question)
