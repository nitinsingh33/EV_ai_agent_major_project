from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from core.config import config
from apps.routes import ingest, chat
from core.logging import configure_logging, logger
import uuid
from fastapi import Response

app = FastAPI()
configure_logging()

def require_api_key(request: Request):
    api_key = request.headers.get("x-api-key")
    if config.API_KEY and api_key != config.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key."
        )

@app.get("/")
async def root():
    return {"status": "ok", "message": "Backend is live 🚀"}


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/secure-endpoint")
async def secure_endpoint(dep=Depends(require_api_key)):
    return {"message": "You have access."}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error."}
    )

@app.middleware("http")
async def add_request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    logger.info("request_received", method=request.method, url=str(request.url), request_id=request_id)
    response: Response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    logger.info("response_sent", status_code=response.status_code, request_id=request_id)
    return response

app.include_router(ingest.router)
app.include_router(chat.router)