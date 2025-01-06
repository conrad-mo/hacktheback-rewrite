from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import Session
from app.core.db import create_db_and_tables, seed_questions, engine
from app.routers import router

questions = [
    {"label": "First Name", "required": True},
    {"label": "Last Name", "required": True},
    {"label": "Email", "required": True},
    {"label": "Phone Number", "required": True},
    {"label": "Country", "required": True},
    {"label": "School Name", "required": True},
    {"label": "Current Level of Study", "required": True},
    {"label": "Major", "required": True},
    {"label": "Expected Graduation Year", "required": True},
]


def get_application():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router, prefix="/api")

    return app


app = get_application()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        seed_questions(questions, session)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
