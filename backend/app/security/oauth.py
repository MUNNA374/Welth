from fastapi.security import OAuth2PasswordBearer
from backend.app.core.config import settings

# OAuth2 Password Bearer scheme points to the login token endpoint
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)
