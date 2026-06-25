import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Welth Personal Finance Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "SUPER_SECRET_SECURITY_KEY_FOR_JWT_WELTH_2026_DO_NOT_LEAK"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week
    
    # DB & Cache URLs
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/welth"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS Origins
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
    ]

    # Third Party Integrations
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", "MOCK_GEMINI_KEY")
    OPENAI_API_KEY: Optional[str] = None
    CLOUDINARY_URL: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET_NAME: Optional[str] = None

    # Monitoring
    SENTRY_DSN: Optional[str] = None
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
