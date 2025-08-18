import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

# Load environment variables from .env file
load_dotenv()

class Config:
    @property
    def GEMINI_API_KEY(self) -> str:
        value = os.getenv("AIzaSyB1WbRxcGG-BlaFiBkhQTw7h9PVyBXKVm4")
        if not value:
            raise ValueError("GEMINI_API_KEY environment variable is required.")
        return value

    @property
    def QDRANT_URL(self) -> str:
        return os.getenv("QDRANT_URL", "https://be012654-1dc6-4856-950d-04fc5edff456.us-east4-0.gcp.cloud.qdrant.io:6333")

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

config = Config()