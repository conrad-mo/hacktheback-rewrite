from fastapi import APIRouter

from app.routers.account import router as account
from app.routers.forms import router as forms

router = APIRouter()

router.include_router(account, prefix="/account", tags=["account"])
router.include_router(forms, prefix="/forms", tags=["forms"])