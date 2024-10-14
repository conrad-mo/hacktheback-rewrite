from fastapi import APIRouter

router = APIRouter()

@router.get("/account/login", tags=["account"])
async def login():
    return {"username": "fakecurrentuser"}