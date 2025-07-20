import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from requests import Session
from src.crud import get_user_by_username
from src.core import get_db
from src.schemas import UserResponse

SECRET_KEY = os.getenv("SECRET_KEY", "your-default-super-secure-secret") # check where to set this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def create_access_token(data: dict) -> str:
    """
    Creates an access token with the given data and expiration time.
    
    :param data: Data to encode in the token
    :param expires_delta: Expiration time in minutes
    :return: Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def _create_refresh_token(data: dict) -> str:
    """
    Creates a refresh token with the given data and expiration time.
    
    :param data: Data to encode in the token
    :return: Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db)
    ) -> UserResponse:
    """
    Retrieves the current user from the access token.
    
    :param token: Access token
    :return: Decoded token data
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

async def refresh_token(
        refresh_token: str, 
        db: Session = Depends(get_db)
    ) -> str:
    """
    Refreshes the access token using a refresh token.
    
    :param refresh_token: Refresh token
    :return: New access token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    
    new_access_token = _create_refresh_token(data={"sub": user.username})
    return new_access_token
