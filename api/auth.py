from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schemas.user import UserIn, UserOut, UserRole
from core.security import verify_password, create_access_token
from models.user import User
from services.user_service import user_in_to_db, user_db_to_user_out
from schemas.auth import LoginRequest, TokenResponse
from db.deps import get_db
from core.auth import get_current_user as get_current_identity, require_roles

router = APIRouter(tags=["auth"])


@router.get("/auth-check")
def auth_check(identity=Depends(get_current_identity)):
    return {"status": "ok", "identity": identity}


@router.post("/admin-only")
def admin_endpoint(identity=Depends(require_roles(UserRole.ADMIN))):
    return {"msg": "Admin access granted"}

@router.post("/engineer-or-admin")
def engineer_or_admin_endpoint(identity=Depends(require_roles(UserRole.ADMIN, UserRole.ENGINEER))):
    return {"msg": "Engineer or Admin access granted"}


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserIn, db: Session = Depends(get_db)):
    user_db = user_in_to_db(user_in)

    try:
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"User registration failed {e}")
    return user_db_to_user_out(user_db)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"user_id": str(user.id), "role": user.role})
    return TokenResponse(access_token=access_token)
