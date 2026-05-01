from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "changeme"

    # Database — use Supabase PostgreSQL connection URL
    # Format: postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
    database_url: str = "sqlite:///./chatbot_akademik.db"

    # Supabase
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None

    # JWT
    jwt_secret_key: str = "changeme"
    jwt_access_token_expires: int = 3600

    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"

    class Config:
        env_file = ".env"


settings = Settings()
