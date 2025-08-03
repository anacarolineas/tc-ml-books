from fastapi import APIRouter, Depends, HTTPException, Request, status
from requests import Session
from src.core.database import get_db
from src.core.limiter import limiter
from src.crud.users import create_user
from src.schemas import UserCreate, UserResponse

router = APIRouter()

@router.post(
    "/users",
    response_model=UserResponse,
    summary="Create a new user"
)
@limiter.limit("5/minute")
async def register(
    request: Request,
    user_data: UserCreate,
    db: Session = Depends(get_db)
    ) -> UserResponse:
    """
    Endpoint to create a new user.
    
    - Requires username and password.
    - Limits to 5 requests per minute.
    - Returns the created user object.
    """
    new_user = create_user(db, user_data.username, user_data.password)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    return new_user