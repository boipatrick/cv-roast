from pydantic_settings import BaseSettings
from functools import lru_cache
from enum import Enum

class RoastLevel(str, Enum):
    GENTLE = "gentle"
    SAVAGE = "savage"
    BRUTAL = "brutal"
    CONSTRUCTIVE = "constructive"

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/cv_roaster_db"
    
    # LLM APIs
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    PREFERRED_LLM: str = "openai"  # openai, anthropic
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: list = [".pdf", ".docx", ".txt"]
    
    # Redis & Celery
    REDIS_URL: str = "redis://localhost:6379"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # App
    APP_NAME: str = "CV Roaster API"
    DEBUG: bool = False
    API_VERSION: str = "v1"
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]
    
    # Roasting Settings
    DEFAULT_ROAST_LEVEL: RoastLevel = RoastLevel.SAVAGE
    MAX_ROASTS_PER_DAY: int = 50
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
