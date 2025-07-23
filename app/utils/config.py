"""
Configuration management for Text2SQL Assistant
"""
import os
from functools import lru_cache
from typing import Optional
from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # LLM Configuration
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gemini-1.5-flash"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./text2sql_assistant.db"
    DATABASE_ECHO: bool = False
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    
    # Application Settings
    APP_NAME: str = "Text2SQL Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG_MODE: bool = True
    
    # Security
    SECRET_KEY: str = "your_secret_key_here_change_in_production"
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    
    @validator("GEMINI_API_KEY")
    def validate_gemini_key(cls, v):
        if not v:
            print("Warning: GEMINI_API_KEY not set. Please set it for LLM functionality.")
        return v
    
    @property
    def allowed_origins_list(self) -> list[str]:
        """Convert comma-separated origins to list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings() 