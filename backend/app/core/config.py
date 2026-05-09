from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str
    OLLAMA_URL: str = "http://localhost:11434"

    class Config:
        env_file = ".env"

settings = Settings()