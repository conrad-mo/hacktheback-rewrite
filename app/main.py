# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router
from sqlmodel import Session
from app.models import Item
from app.core.db import get_session

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

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/items/")
async def create_item(item: Item, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}
