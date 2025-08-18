import os
from dotenv import load_dotenv 

load_dotenv()

class Config:
    @property
    def GEMINI_API_KEY(self) -> str:
        value = os.getenv("GEMINI_API_KEY")
        if not value:
            raise ValueError("GEMINI_API_KEY environment variable is required.")
        return value

    @property
    def QDRANT_URL(self) -> str:
        return os.getenv(
            "QDRANT_URL",
            "https://add3c7ea-12d3-4ed6-b736-6684ac64deb5.us-east4-0.gcp.cloud.qdrant.io"
        )

    @property
    def QDRANT_API_KEY(self) -> str:
        value = os.getenv("QDRANT_API_KEY")
        if not value:
            raise ValueError("QDRANT_API_KEY environment variable is required.")
        return value

    @property
    def QDRANT_COLLECTION(self) -> str:
        return os.getenv("QDRANT_COLLECTION", "default_collection")

    @property
    def API_KEY(self) -> str:
        return os.getenv("API_KEY", "")

    @property
    def EMBED_MODEL(self) -> str:
        return os.getenv("EMBED_MODEL", "default_model")

    @property
    def SAFE_MODE(self) -> bool:
        return os.getenv("SAFE_MODE", "false").lower() == "true"

    @property
    def POSTGRES_URL(self) -> str:
        return os.getenv("POSTGRES_URL")

    @property
    def POSTGRES_DSN(self) -> str:
        return os.getenv("POSTGRES_DSN")

config = Config()
