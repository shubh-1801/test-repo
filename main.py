import hashlib
import os
import secrets
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


STATIC_DIR = Path(__file__).resolve().parent / "static"
app = FastAPI(title="FastAPI", version="0.1.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class Body(BaseModel):
    content: str = Field(examples=["Hello, world!"])


class TokenResponse(BaseModel):
    token: str


class ChecksumResponse(BaseModel):
    checksum: str


@app.get("/", response_class=FileResponse, summary="Root")
def root():
    return FileResponse(STATIC_DIR / "index.html", media_type="text/html")


@app.post("/generate", response_model=TokenResponse, summary="Generate")
def generate(body: Body):
    """Generate a random, URL-safe token for a submitted text request.

    Each request returns a new opaque token, not a digest of the content.
    Tokens are not stored and are not authentication credentials.
    """
    return TokenResponse(token=secrets.token_urlsafe(32))


@app.post("/checksum", response_model=ChecksumResponse, summary="Calculate Checksum")
def checksum(body: Body):
    """Calculate the MD5 checksum of the provided UTF-8 text.

    Example POST request body: {"content": "Hello, world!"}

    MD5 is used for compatibility with the illustrated 32-character checksum,
    not for password hashing or security-sensitive integrity verification.
    """
    digest = hashlib.md5(body.content.encode("utf-8"), usedforsecurity=False)
    return ChecksumResponse(checksum=digest.hexdigest())


@app.get("/source", include_in_schema=False)
def source():
    source_url = os.getenv("PROJECT_SOURCE_URL")
    if source_url and source_url.startswith(("https://", "http://")):
        return RedirectResponse(source_url)
    return FileResponse(Path(__file__).resolve(), media_type="text/plain")