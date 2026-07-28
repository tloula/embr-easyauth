# TEST-ONLY app: intentionally echoes all headers and must not run in production.
#
# This Azure Functions app is a thin ASGI host for the FastAPI app in `app/main.py`,
# so both deployments serve byte-identical pages, routes, and behaviour.

from __future__ import annotations

import sys
from pathlib import Path

# The shared `app` package lives at the repo root during local development, and is
# vendored into this folder when the function app is packaged for deployment (see
# README). Adding the repo root to sys.path makes `func start` work straight from a
# clone without a copy step; the vendored copy wins once it exists.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.append(str(_REPO_ROOT))

import azure.functions as func  # noqa: E402

from app.main import app as fastapi_app  # noqa: E402

app = func.AsgiFunctionApp(app=fastapi_app, http_auth_level=func.AuthLevel.ANONYMOUS)
