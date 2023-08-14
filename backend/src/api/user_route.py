from fastapi import APIRouter, Depends, HTTPException, status
from ..db.user_db import DatabaseManager
from ..models.user_models import UserIn, UserOut, RegisterUser
from ..utils.auth import get_current_user, get_current_user_role, get_token
from ..utils.auth_service import AuthService
from ..models.roles import UserRole
from dotenv import load_dotenv
import os
from logger import get_logger

load_dotenv()

API_KEY = os.getenv('AIRTABLE_API_KEY')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')

router = APIRouter()
db_manager = DatabaseManager(BASE_ID, API_KEY, TABLE_NAME)
log = get_logger(__name__)
# log = get_logger("user_route")

@router.post("/users/")
def create_user(user_data: dict):
    log.debug("creating user with username:%s", user_data)
    return db_manager.add_user(user_data)

@router.get("/users/{username}")
def get_user(username: str):
    log.debug("Retrieving user with username:%s", username)
    return db_manager.get_user(username=username)

@router.put("/users/update/{record_id}")
def update_user(record_id: str, user_data: dict):
    log.debug("Updating user with record_id:%s", record_id)
    return db_manager.update_user(record_id, user_data)

@router.delete("/users/delete/{record_id}")
def delete_user(record_id: str):
    success = db_manager.delete_user(record_id)
    log.debug("Deleting user with record_id:%s", record_id)
    return {"success": success}

@router.post("/register/")
async def register_user(user: UserIn, auth_service: AuthService = Depends(AuthService)):
    log.debug("User data received: %s", user.dict())
    
    existing_user = db_manager.get_user(username=user.username)
    if existing_user:
        log.debug("User with username:%s already exists", user.username)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    hashed_password = auth_service.get_password_hash(user.password)
    log.debug("Password hashed successfully for username:%s", user.username)

    user_data = {"Username": user.username, "PasswordHash": hashed_password}
    db_manager.add_user(user_data)
    log.debug("User with username:%s added successfully", user.username)
    
    return get_token(user.username)

@router.post("/login/", response_model=dict)
async def login(user: UserIn, auth_service: AuthService = Depends(AuthService)):
    db_user = db_manager.get_user(username=user.username)
    if not db_user or not auth_service.verify_password(user.password, db_user["PasswordHash"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    return get_token(user.username)

@router.get("/users/me/", response_model=UserOut)
async def read_users_me(current_user: str = Depends(get_current_user)):
    user = db_manager.get_user(username=current_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user["Username"], "email": user["Email"]}  # Adjust as per your UserOut model

@router.get("/admin/dashboard/")
async def admin_dashboard(current_user_role: UserRole = Depends(get_current_user_role)):
    if current_user_role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"detail": "Welcome to the admin dashboard!"}
