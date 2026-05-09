from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    ollama_url: str = "http://localhost:11434"

    class Config:
        env_file = ".env"

settings = Settings()