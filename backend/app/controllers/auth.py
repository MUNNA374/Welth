from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.services.auth_service import AuthService
from backend.app.api.deps import get_current_user
from pydantic import BaseModel, EmailStr
from typing import Optional, Any

router = APIRouter()
auth_service = AuthService()

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: UserRegister):
    user = await auth_service.register_user(
        email=user_in.email,
        password=user_in.password,
        first_name=user_in.firstName,
        last_name=user_in.lastName
    )
    return {"id": user.id, "email": user.email, "message": "User registered successfully"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    auth_data = await auth_service.authenticate_user(
        email=form_data.username,
        password=form_data.password
    )
    return {
        "access_token": auth_data["access_token"],
        "token_type": auth_data["token_type"]
    }

@router.get("/me")
async def read_users_me(current_user: Any = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "firstName": current_user.firstName,
        "lastName": current_user.lastName,
        "role": current_user.role
    }
