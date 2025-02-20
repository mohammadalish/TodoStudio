from datetime import datetime, timedelta, timezone
from fastapi import (
    status,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import (OAuth2PasswordRequestForm as LoginForm,
                              OAuth2PasswordBearer as Bearer)
from jose import jwt, JWTError
from typing import Annotated
from models import Users

# Dependencies
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ouath2_bearer = Bearer(tokenUrl="auth/token")
bearer_dependency = Annotated[str, Depends(ouath2_bearer)]

# Functions


async def get_current_user(token: bearer_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not VALIDATE credentials",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not VALIDATE credentials",
        )
    return


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

# JWT
SECRET_KEY = "04fe417dedfd59a08cb1f3aec290f852c9b878068cc5fc514b815e9fa21acbc8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20


def create_access_token(username: str, user_id: int, expires_delta: int):
    """Creates a JWT token with expiration."""
    encode = {"sub": username, "id": user_id}

    # Ensure expires_delta is converted to timedelta
    expires = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)

    encode.update({"exp": expires})
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return token
