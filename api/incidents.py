from fastapi import APIRouter, Depends
from core.auth import get_current_user

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.get("/protected-test")
def protected_test(current_user: dict = Depends(get_current_user)):
    return {"message": "You are authenticated", "user": current_user}
