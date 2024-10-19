from fastapi import Depends, APIRouter, HTTPException, status, Security
from typing import Annotated
from app.models.token import TokenData

from app.routers.account import decode_jwt
from app.routers.account import router as account
from app.routers.forms import router as forms
from app.routers.admin import router as admin

router = APIRouter()

def is_admin(token_data: Annotated[TokenData, Security(decode_jwt, scopes=["admin"])]) -> bool:
    if "admin" not in token_data.scopes:
      raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User does not permission"
        )
    return True

router.include_router(account, prefix="/account", tags=["account"])
router.include_router(forms, prefix="/forms", tags=["forms"])
router.include_router(admin, prefix="/admin", tags=["admin"], dependencies=[Depends(is_admin)])