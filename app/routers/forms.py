from fastapi import APIRouter

router = APIRouter()

@router.post("/forms/save", tags=["forms"])
async def save():
    return {"username": "fakecurrentuser"}

@router.post("/forms/submit", tags=["forms"])
async def submit():
    return {"username": "fakecurrentuser"}
