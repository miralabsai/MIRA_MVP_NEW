# services/auth_service.py
from argon2 import PasswordHasher
from pydantic import EmailStr
from dataclasses import dataclass
from logger import get_logger

logger = get_logger(__name__)

@dataclass
class User:
    username: EmailStr
    password: str

class AuthService:
    pwd_context = PasswordHasher()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        logger.debug("Verifying password...")
        logger.debug("Plain password: %s", plain_password)
        logger.debug("Hashed password: %s", hashed_password)
        try:
            self.pwd_context.verify(hashed_password, plain_password)
            is_password_correct = True
        except Exception as e:
            logger.debug("Exception during verification: %s", str(e))
            is_password_correct = False
        logger.debug("Password correct? %s", is_password_correct)
        return is_password_correct

    def get_password_hash(self, password: str) -> str:
        logger.debug("Hashing password...")
        hashed_password = self.pwd_context.hash(password)
        logger.debug("Password hashed: %s", hashed_password)
        return hashed_password
