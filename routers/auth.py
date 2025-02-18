from fastapi import (
    APIRouter,
    status,
)
from schemas import CreateUserRequest, UserResponse
from passlib.context import CryptContext
from models import Users
from database import get_db, db_dependency

router = APIRouter(prefix="/auth", tags=["Athentication"],)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    db: db_dependency, create_user_request: CreateUserRequest
) -> UserResponse:
    create_user_model = Users(
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        email=create_user_request.email,
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        is_active=True,
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return create_user_model
