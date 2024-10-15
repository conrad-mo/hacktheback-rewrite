from fastapi import APIRouter

router = APIRouter()

@router.get("/getusers")
async def getusers():
    return {"username": "fakecurrentuser-admin"}