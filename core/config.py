import os
from pydantic_settings import BaseSettings  # ✅ new import

class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "dev")
    API_KEY: str = os.getenv("API_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "")
    POSTGRES_DSN: str = os.getenv("POSTGRES_DSN", "")
    EMBED_MODEL: str = os.getenv("EMBED_MODEL", "")
    VECTORSTORE_PATH: str = os.getenv("VECTORSTORE_PATH", "")
    SAFE_MODE: str = os.getenv("SAFE_MODE", "")

    class Config:
        env_file = ".env"
        case_sensitive = True

config = Settings()
