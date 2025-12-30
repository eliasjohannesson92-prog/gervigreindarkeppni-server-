import os
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from challenges.dispatch import dispatch_predict

try:
    from . import build_info  # generated during deploy
except Exception:
    build_info = None

app = FastAPI()


class PredictRequest(BaseModel):
    text: Optional[str] = None
    image_b64: Optional[str] = None
    rl_state: Optional[dict[str, Any]] = None
    extra: Optional[dict[str, Any]] = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    challenge = os.getenv("CHALLENGE", "nlp").lower()

    git_sha = os.getenv("GIT_SHA", "unknown")
    model_version = os.getenv("MODEL_VERSION", "stub-0")

    if build_info is not None:
        git_sha = getattr(build_info, "GIT_SHA", git_sha)
        model_version = getattr(build_info, "MODEL_VERSION", model_version)

    return {
        "git_sha": git_sha,
        "challenge": challenge,
        "model_version": model_version,
    }


@app.post("/predict")
def predict(req: PredictRequest):
    challenge = os.getenv("CHALLENGE", "nlp").lower()
    try:
        result = dispatch_predict(challenge, req.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"challenge": challenge, "result": result}


@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs", "health": "/health", "version": "/version"}
