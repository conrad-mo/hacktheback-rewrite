from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
async def login():
    return {"username": "fakecurrentuser"}

@router.post("/signup")
async def signup():
    return {"username": "fakecurrentuser"}

@router.put("/verify")
async def verify():
    return {"username": "fakecurrentuser"}

@router.get("/reset_password")
async def reset_password():
    return {"username": "fakecurrentuser"}

@router.post("/refresh")
async def refresh():
    return {"username": "fakecurrentuser"}