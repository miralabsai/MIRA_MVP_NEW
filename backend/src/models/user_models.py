# user_models.py
from pydantic import BaseModel, EmailStr
from .roles import UserRole

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
    username: EmailStr
    first_name: str
    last_name: str
    role: UserRole

