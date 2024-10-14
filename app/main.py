# main.py
from fastapi import FastAPI
from .routers import account, forms

app = FastAPI()

app.include_router(account.router)
app.include_router(forms.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}
