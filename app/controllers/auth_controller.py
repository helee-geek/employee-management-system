from app.schemas.user_schema import UserCreate, UserLogin
from app.services.auth_service import register_user, login_user, refresh_access_token

def register_controller(db, user_data: UserCreate):
    return register_user(db, user_data)

def login_controller(db, credentials: UserLogin):
    return login_user(db, credentials)

def refresh_controller(db, refresh_token: str):
    return refresh_access_token(db, refresh_token)

