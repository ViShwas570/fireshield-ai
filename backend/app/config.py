"""FireShield AI - Configuration."""
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    secret_key: str = os.getenv("SECRET_KEY", "fireshield-ai-secret-key-2025")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours

settings = Settings()
