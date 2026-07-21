# embr-easyauth

A deliberately minimal, **test-only** Python FastAPI app that echoes incoming request headers. It exists to verify that the Embr YARP proxy strips spoofable EasyAuth and forwarding headers before requests reach an app.

## Stack

- [uv](https://docs.astral.sh/uv/) for project & dependency management
- FastAPI + uvicorn

## Run locally

```sh
uv sync
uv run uvicorn app.main:app --port 8000
```

Open http://localhost:8000 to inspect every header received by the app in a browser. EasyAuth-related identity headers are highlighted for quick verification. Use `/headers` when a raw JSON response is more convenient for automation.

## Routes

| Method | Path | Description |
| --- | --- | --- |
| GET | `/` | HTML request inspector showing request metadata and all received headers |
| GET/POST/PUT/DELETE | `/headers` | Echoes request method, path, all headers, and client host as JSON |
| GET | `/health` | Liveness probe (`{"status":"ok"}`) |

## ⚠ Security warning

The homepage and `/headers` dump **all request headers without redaction**, including any credentials or cookies sent by a client. This is intentional for direct proxy-stripping and EasyAuth injection tests and must **never** run in production or in any environment receiving real user traffic.
