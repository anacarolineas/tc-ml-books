from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from src.core import get_db
from src.crud.users import create_user
from src.schemas import UserCreate, UserResponse

router = APIRouter()

@router.post(
    "/users",
    response_model=UserResponse,
    summary="Create a new user"
)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    ) -> UserResponse:
    """
    Endpoint to create a new user.
    
    - Requires username and password.
    - Returns the created user object.
    """
    new_user = create_user(db, user_data.username, user_data.password)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    return new_user