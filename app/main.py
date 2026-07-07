# TEST-ONLY app: intentionally echoes all headers and must not run in production.

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="embr-easyauth", version="0.1.0")


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "embr-easyauth",
        "purpose": "Test-only header echo app for validating Embr proxy header stripping.",
        "headersEndpoint": "/headers",
    }


@app.api_route("/headers", methods=["GET", "POST", "PUT", "DELETE"])
def echo_headers(request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "method": request.method,
            "path": request.url.path,
            "headers": dict(request.headers),
            "client": request.client.host if request.client else None,
        }
    )


@app.get("/health")
def healthz() -> dict[str, str]:
    return {"status": "ok"}

