# test_auth_service.py
from auth_service import AuthService

def test_auth_service():
    auth_service = AuthService()

    # Test password hashing
    password = "my_password"
    hashed_password = auth_service.get_password_hash(password)
    print(f"Hashed password: {hashed_password}")

    # Test password verification
    is_password_correct = auth_service.verify_password(password, hashed_password)
    print(f"Is password correct? {is_password_correct}")

    # Test incorrect password
    is_password_correct = auth_service.verify_password("wrong_password", hashed_password)
    print(f"Is password correct? {is_password_correct}")

if __name__ == "__main__":
    test_auth_service()
