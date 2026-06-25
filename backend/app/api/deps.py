from fastapi import Depends, HTTPException, status
from backend.app.security.oauth import oauth2_scheme
from backend.app.security.jwt import verify_access_token
from backend.app.repositories.user_repository import UserRepository
from backend.app.core.db import db
from typing import Any

user_repo = UserRepository()

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Any:
    """Decodes the JWT token to retrieve and verify the active user from the database."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user_id = verify_access_token(token)
    if user_id is None:
        raise credentials_exception
        
    user = await user_repo.get(user_id)
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_active_admin(current_user: Any = Depends(get_current_user)) -> Any:
    """RBAC checker ensuring the current authenticated user has administrative privileges."""
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted. Administrative access required."
        )
    return current_user
