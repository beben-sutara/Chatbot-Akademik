from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from supabase import create_client, Client
from .config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Supabase client — available when SUPABASE_URL and SUPABASE_KEY are set.
# Use this for Supabase-specific features (Storage, Realtime, Edge Functions, etc.).
supabase: Client | None = None
if settings.supabase_url and settings.supabase_key:
    supabase = create_client(settings.supabase_url, settings.supabase_key)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_supabase() -> Client:
    """FastAPI dependency — yields the Supabase client."""
    if supabase is None:
        raise RuntimeError(
            "Supabase client not initialised. "
            "Set SUPABASE_URL and SUPABASE_KEY in your .env file."
        )
    return supabase
