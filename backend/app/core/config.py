import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Hiring Agent"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./backend/data/hiring.db")

    class Config:
        case_sensitive = True

settings = Settings()