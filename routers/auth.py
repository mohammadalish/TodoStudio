from fastapi import (
    APIRouter,
    HTTPException,
    status,
)
from utils.auth_utils import (
    authenticate_user,
    bcrypt_context,
    auth_dependency,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES as atem,
)
from models import Users
from database import db_dependency
from schemas import (CreateUserRequest, UserResponse, Token)

router = APIRouter(prefix="/auth", tags=["Athentication"],)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_single_user(
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


@router.post(
    "/token", status_code=status.HTTP_201_CREATED,
    response_model=Token
)
async def login_for_access_token(
    form_data: auth_dependency,
    db: db_dependency
):
    user = authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db=db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(
        username=user.username, user_id=user.id, expires_delta=atem)
    return {
        "access_token": token,
        "token_type": "bearer"
    }
