# embr-easyauth

A deliberately minimal, **test-only** Python FastAPI app that echoes incoming request headers. It exists to verify that the Embr YARP proxy strips spoofable EasyAuth and forwarding headers before requests reach an app.

The same app ships in two flavours that share one code base:

| Flavour | Entry point | Notes |
| --- | --- | --- |
| Embr / container | [app/main.py](app/main.py) | Run by [embr.yaml](embr.yaml) and the root [Dockerfile](Dockerfile) via uvicorn |
| Azure Functions | [functionapp/function_app.py](functionapp/function_app.py) | Hosts the identical FastAPI app through `azure.functions.AsgiFunctionApp` |

## Stack

- [uv](https://docs.astral.sh/uv/) for project & dependency management
- FastAPI + uvicorn

## Run locally

```sh
uv sync
uv run uvicorn app.main:app --port 8000
```

Open http://localhost:8000 to inspect every header and cookie received by the app in a browser. Cookie entries remain in browser order and duplicate names are preserved, which matters when the same cookie name exists at different paths. EasyAuth-related identity headers are highlighted for quick verification, the `x-ms-client-principal` header is base64-decoded server-side into a formatted claims table, and the page fetches `/.auth/me` client-side to render the signed-in identity, its provider, and a formatted claims table (with the raw JSON available in a collapsible section). When EasyAuth is not enabled or the caller is unauthenticated, those panels report the missing header or failing status instead. Use `/auth` or `/auth/cookies` to exercise the same inspector under the `/auth` path boundary, and use `/headers` when a raw JSON response is more convenient for automation.

## Routes

| Method | Path | Description |
| --- | --- | --- |
| GET | `/` | HTML request inspector showing request metadata, the decoded `x-ms-client-principal`, `/.auth/me` identity, and all received cookies and headers |
| GET | `/auth` | Same inspector page under the `/auth` boundary for testing path-scoped cookies |
| GET | `/auth/cookies` | Same inspector page under the `/auth` boundary for testing path-scoped cookies |
| GET/POST/PUT/DELETE | `/headers` | Echoes request method, path, all cookies and headers, client host, and the decoded `x-ms-client-principal` as JSON |
| GET | `/health` | Liveness probe (`{"status":"ok"}`) |

Both flavours expose the same routes. The Functions host sets `routePrefix` to `""` in [functionapp/host.json](functionapp/host.json), so there is no `/api` prefix and the paths match the Embr deployment exactly.

## Azure Functions flavour

[functionapp/function_app.py](functionapp/function_app.py) is a thin ASGI host — it imports the FastAPI app from `app/main.py` rather than reimplementing anything, so behaviour cannot drift between the two deployments. All HTTP triggers are anonymous, which lets platform EasyAuth own authentication.

### Run locally

Requires [Azure Functions Core Tools v4](https://learn.microsoft.com/azure/azure-functions/functions-run-local).

```sh
cd functionapp
pip install -r requirements.txt
func start
```

`function_app.py` appends the repo root to `sys.path`, so the shared `app` package resolves straight from a clone with no copy step.

### Deploy as a container

Build from the repo root so the shared `app` package is in the build context:

```sh
docker build -f functionapp/Dockerfile -t embr-easyauth-func .
```

### Deploy as a zip (manual push)

`func` only packages its own project folder, so the shared `app` package is staged alongside the Functions files. `host.json` must sit at the zip root:

```powershell
$stage = Join-Path $env:TEMP "embr-func-stage"
Remove-Item -Recurse -Force $stage -EA SilentlyContinue
New-Item -ItemType Directory -Path $stage | Out-Null
Copy-Item functionapp\function_app.py, functionapp\host.json, functionapp\requirements.txt $stage
Copy-Item -Recurse app "$stage\app"
New-Item -ItemType Directory -Force dist | Out-Null
Compress-Archive -Path "$stage\*" -DestinationPath dist\functionapp.zip -Force
```

Push it to the `embr-easyauth` function app (Flex Consumption, Python 3.14, resource group `easyauth`):

```sh
az functionapp deployment source config-zip --subscription e2161017-4eef-4198-ab67-10f3e7a868b2 --resource-group easyauth --name embr-easyauth --src dist/functionapp.zip
```

Flex Consumption always remote-builds from `requirements.txt`, so no `SCM_DO_BUILD_DURING_DEPLOYMENT` setting is needed. The deployed app is served from https://embr-easyauth-bsbnhta7cyemfzes.canadacentral-01.azurewebsites.net.

## ⚠ Security warning

The homepage, `/auth`, `/auth/cookies`, and `/headers` dump **all request headers without redaction**, including any credentials or cookies sent by a client. This is intentional for direct proxy-stripping and EasyAuth injection tests and must **never** run in production or in any environment receiving real user traffic.

Use this app only for private boundary testing: `/` can reveal a domain-scoped `embr_access_token`, while `/auth/cookies` can reveal `embr_refresh_token` when its cookie `Path` is `/auth`. `HttpOnly` blocks browser JavaScript from reading cookies, but it does not stop a browser from sending them to an attacker-controlled server.
