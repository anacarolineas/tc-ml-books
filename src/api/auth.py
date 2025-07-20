from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from requests import Session
from src.core import get_db
from src.core import create_access_token
from src.crud import authenticate_user
from src.schemas import TokenResponse

router = APIRouter()

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login to obtain an access token"
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    Logs in a user and returns an access token.
    
    - Requires username and password.
    - Returns a JWT token if successful.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=access_token, token_type="bearer")
    