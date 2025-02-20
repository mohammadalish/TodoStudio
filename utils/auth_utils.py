from datetime import datetime, timedelta
from fastapi import Depends
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm as LoginForm
from jose import jwt
from typing import Annotated

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(user.hashed_password, password):
        return False
    return user


auth_dependency = Annotated[LoginForm, Depends()]

# JWT
SECTER_KEY = "04fe417dedfd59a08cb1f3aec290f852c9b878068cc5fc514b815e9fa21acbc8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(datetime.timezone.utc) + expires_delta
    encode.update({"exp": expires})
    token = jwt.encode(encode, SECTER_KEY, algorithm=ALGORITHM)
    return token
