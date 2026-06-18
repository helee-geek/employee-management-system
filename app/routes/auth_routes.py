from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin
from app.schemas.token_schema import Token, RefreshTokenRequest
from app.controllers.auth_controller import register_controller, login_controller, refresh_controller
from app.dependencies.auth_dependency import get_current_user, require_role
from app.models.user_model import User, RoleEnum

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return register_controller(db, user_data)

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    return login_controller(db, credentials)

@router.post("/refresh", response_model=Token)
def refresh(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    return refresh_controller(db, payload.refresh_token)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/admin-only")
def admin_test(current_user: User = Depends(require_role(RoleEnum.admin))):
    return {"message": f"Welcome, admin {current_user.name}"}