from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from core.config import config
from apps.routes import ingest, chat
from core.logging import configure_logging, logger
import uuid

app = FastAPI()
configure_logging()

# --- API Key check middleware ---
def require_api_key(request: Request):
    api_key = request.headers.get("x-api-key")
    if config.API_KEY and api_key != config.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return True

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    logger.info(f"Request ID={request_id} | Method={request.method} | URL={request.url}")
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Request ID={request_id} | Exception: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})
    logger.info(f"Request ID={request_id} | Completed with status {response.status_code}")
    return response

# --- Routes register ---
app.include_router(ingest.router, prefix="/ingest", tags=["Ingest"], dependencies=[Depends(require_api_key)])
app.include_router(chat.router, prefix="/chat", tags=["Chat"], dependencies=[Depends(require_api_key)])

@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI backend is running 🚀"}
