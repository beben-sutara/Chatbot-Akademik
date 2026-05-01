from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "changeme"

    # Database
    database_url: str = "sqlite:///./chatbot_akademik.db"

    # JWT
    jwt_secret_key: str = "changeme"
    jwt_access_token_expires: int = 3600

    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"

    class Config:
        env_file = ".env"


settings = Settings()
