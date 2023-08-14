# roles.py
from enum import Enum

class UserRole(str, Enum):
    CONSUMER = "Consumer"
    LOAN_OFFICER = "Loan Officer"
    ADMIN = "Admin"
