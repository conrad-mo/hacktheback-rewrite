from fastapi import APIRouter

router = APIRouter()

@router.post("/account/login", tags=["account"])
async def login():
    return {"username": "fakecurrentuser"}

@router.post("/account/signup", tags=["account"])
async def signup():
    return {"username": "fakecurrentuser"}

@router.put("/account/verify", tags=["account"])
async def verify():
    return {"username": "fakecurrentuser"}

@router.get("/account/reset_password", tags=["account"])
async def reset_password():
    return {"username": "fakecurrentuser"}

@router.post("/account/refresh", tags=["account"])
async def refresh():
    return {"username": "fakecurrentuser"}