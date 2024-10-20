# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import create_db_and_tables
from app.routers import router
from app.models.forms import Forms_Question

questions = [
    "First Name",
    "Last Name",
    "Email",
    "Phone Number",
    "Country",
    "School Name",
    "Current Level of Study",
    "Major",
    "Expected Graduation Year",
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


def create_questions():
    for i in range(len(questions)):
        form_question = Forms_Question(
            order=i,
            label=questions[i],
        )


app = get_application()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def read_root():
    return {"Hello": "World"}
