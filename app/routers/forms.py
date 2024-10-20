from fastapi import APIRouter

router = APIRouter()


@router.post("/create")
async def create():
    return {"username": "fakecurrentuser"}


@router.post("/save")
async def save():
    return {"username": "fakecurrentuser"}


@router.post("/submit")
async def submit():
    return {"username": "fakecurrentuser"}
