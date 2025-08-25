from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union
import json
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # Ignore unknown environment variables
    )

    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Smart Summary App - Backend API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Scalable FastAPI backend with Google Gemini AI integration for intelligent text summarization"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = ENVIRONMENT == "development"

    # CORS - can be set as JSON string in environment
    ALLOWED_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:3003",
        "http://localhost:3004",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3003",
        "http://127.0.0.1:3004",
        "http://127.0.0.1:8080",
    ]
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse ALLOWED_ORIGINS from string or list"""
        if isinstance(self.ALLOWED_ORIGINS, str):
            try:
                # Try to parse as JSON string
                return json.loads(self.ALLOWED_ORIGINS)
            except json.JSONDecodeError:
                # If not JSON, split by comma and clean up
                return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]
        return self.ALLOWED_ORIGINS

    # Gemini Configuration
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"
    GEMINI_MAX_TOKENS: int = 100000
    GEMINI_TEMPERATURE: float = 0.7
    
    # Streaming Configuration
    STREAMING_CHUNK_SIZE: int = 2  # Words per chunk (optimized for word-by-word effect)
    STREAMING_DELAY_MS: int = 50   # Delay between chunks in milliseconds (human-like typing speed)

    # Logging
    LOG_LEVEL: str = "INFO"


settings = Settings()
