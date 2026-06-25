from datetime import timedelta
from typing import Optional, Dict, Any
from backend.app.repositories.user_repository import UserRepository
from backend.app.security.jwt import get_password_hash, verify_password, create_access_token
from backend.app.security.audit import log_audit_event
from backend.app.core.db import db
from fastapi import HTTPException, status

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def register_user(self, email: str, password: str, first_name: Optional[str] = None, last_name: Optional[str] = None) -> Any:
        # Check if user already exists
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email is already registered."
            )
        
        hashed_password = get_password_hash(password)
        
        # Start a transaction to create User and Settings
        user = await self.user_repo.create({
            "email": email,
            "passwordHash": hashed_password,
            "firstName": first_name,
            "lastName": last_name,
            "role": "USER"
        })
        
        # Create default settings for user
        await db.settings.create(data={"userId": user.id})
        
        await log_audit_event(action="USER_REGISTRATION", user_id=user.id, details=f"User {email} registered.")
        return user

    async def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.passwordHash):
            await log_audit_event(action="FAILED_LOGIN", details=f"Failed login attempt for {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token = create_access_token(subject=user.id)
        await log_audit_event(action="SUCCESSFUL_LOGIN", user_id=user.id)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }
