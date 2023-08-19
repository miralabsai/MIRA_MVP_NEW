# user_models.py
from pydantic import BaseModel, EmailStr
from .roles import UserRole
from typing import Optional

class UserIn(BaseModel):
    username: EmailStr
    password: str

class RegisterUser(UserIn):
    first_name: str
    last_name: str
    confirm_password: str
    role: UserRole

class UserLogin(BaseModel):
    username: EmailStr
    password: str

class UserOut(BaseModel):
    record_id: str
    username: EmailStr
    first_name: str
    last_name: str
    role: UserRole

class UserUpdate(BaseModel):
    Username: Optional[str]
    Full_Name: Optional[str]
    Phone_Number: Optional[int]
    User_Type: Optional[str]
    NMLS_ID_if_Loan_Officer: Optional[int]
    Notification_Preferences: Optional[str]
