from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Environment
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "YiCe"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./yice.db"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"
    
    @property
    def is_staging(self) -> bool:
        return self.ENVIRONMENT == "staging"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"


# Create global settings instance
settings = Settings()
