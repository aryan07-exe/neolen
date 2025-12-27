from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Health Tracker"
    MONGODB_URL: str
    DATABASE_NAME: str = "health_db"
    GOOGLE_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
