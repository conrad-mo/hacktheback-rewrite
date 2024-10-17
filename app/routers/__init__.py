from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from app.models import UserPublic, Account_User

from app.routers.account import get_current_user
from app.routers.account import router as account
from app.routers.forms import router as forms
from app.routers.admin import router as admin

router = APIRouter()

def is_admin(current_user: Annotated[Account_User, Depends(get_current_user)]) -> UserPublic:
    if not current_user.role == "admin":
      raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User does not permission"
        )
    return current_user

router.include_router(account, prefix="/account", tags=["account"])
router.include_router(forms, prefix="/forms", tags=["forms"])
router.include_router(admin, prefix="/admin", tags=["admin"], dependencies=[Depends(is_admin)])