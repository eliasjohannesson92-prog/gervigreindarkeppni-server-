import logging
import os
import sys
import uuid
from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from challenges.dispatch import dispatch_predict

try:
    from . import build_info  # generated during deploy
except Exception:
    build_info = None

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='{"time":"%(asctime)s", "level":"%(levelname)s", "request_id":"%(request_id)s", "message":"%(message)s"}',
    stream=sys.stdout
)


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        
        # Add request_id to logging context
        old_factory = logging.getLogRecordFactory()
        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            record.request_id = request_id
            return record
        logging.setLogRecordFactory(record_factory)
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        # Restore original factory
        logging.setLogRecordFactory(old_factory)
        return response


app = FastAPI()
app.add_middleware(RequestIDMiddleware)


class PredictRequest(BaseModel):
    inputs: Any


class PredictResponse(BaseModel):
    outputs: Any


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    challenge = os.getenv("CHALLENGE", "unknown")

    git_sha = getattr(build_info, "GIT_SHA", None) if build_info else None
    git_sha = git_sha or os.getenv("GIT_SHA", None)

    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    return {
        "status": "ok",
        "git_sha": git_sha,
        "python_version": python_version,
        "challenge": challenge,
    }


@app.post("/predict")
def predict(req: PredictRequest, request: Request) -> PredictResponse:
    logging.info(f"Received predict request")
    
    # For now, return a simple echo response as a placeholder
    # The actual implementation will depend on the specific challenge
    return PredictResponse(outputs=req.inputs)


@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs", "health": "/health", "version": "/version"}
