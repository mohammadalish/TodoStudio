from typing import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm as LoginForm
from fastapi import Depends
from sqlalchemy.orm import Session
from models import Users

# Dependencies
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Functions


def get_password_hash(password: str):
    """Hashes the password before storing it in the database."""
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies the password during login."""
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    """Authenticates a user by checking the password."""
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):  # Use `verify_password`
        return None
    return user


auth_dependency = Annotated[LoginForm, Depends()]
