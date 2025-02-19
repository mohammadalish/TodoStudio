from fastapi import Depends
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm as LoginForm
from typing import Annotated

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(user.hashed_password, password):
        return False
    return True


auth_dependency = Annotated[LoginForm, Depends()]
