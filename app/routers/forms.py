from fastapi import APIRouter

router = APIRouter()


@router.post("/save")
async def save():
    return {"username": "fakecurrentuser"}


@router.post("/submit")
async def submit():
    return {"username": "fakecurrentuser"}
