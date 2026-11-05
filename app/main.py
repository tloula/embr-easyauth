# Embr EasyAuth Diagnostic App test

from __future__ import annotations

import base64
import binascii
import json
from html import escape
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from app.page import FAVICON, FONTS, LOGO, SCRIPT, STYLE

app = FastAPI(title="embr-easyauth", version="0.1.0")

_EASYAUTH_HEADER_PREFIXES = (
    "x-ms-client-principal",
    "x-ms-token-",
    "x-embr-",
    "x-adc-",
)
_PLATFORM_COOKIE_NAMES = {
    "embr_access_token",
    "embr_refresh_token",
}
_COLLAPSED_VALUE_LENGTH = 160

_GITHUB_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 .7a11.5 11.5 0 0 '
    "0-3.6 22.4c.6.1.8-.3.8-.6v-2.2c-3.3.7-4-1.4-4-1.4-.5-1.4-1.3-1.8-1.3-1.8-1.1-.7.1-.7.1-.7 "
    "1.2.1 1.8 1.2 1.8 1.2 1.1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-5.7 0-1.3.5-2.3 "
    "1.2-3.1-.1-.3-.5-1.6.1-3.1 0 0 1-.3 3.2 1.2a11 11 0 0 1 5.8 0C16.9 4.8 18 5.1 18 5.1c.6 1.5.2 "
    "2.8.1 3.1.8.8 1.2 1.8 1.2 3.1 0 4.4-2.8 5.4-5.5 5.7.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A11.5 11.5 "
    '0 0 0 12 .7Z"/></svg>'
)
_MICROSOFT_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#f35325" d="M1 1h10v10H1z"/>'
    '<path fill="#81bc06" d="M13 1h10v10H13z"/><path fill="#05a6f0" d="M1 13h10v10H1z"/>'
    '<path fill="#ffba08" d="M13 13h10v10H13z"/></svg>'
)
_SIGN_OUT_ICON = (
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5"/>'
    '<path d="M21 12H9"/></svg>'
)
_CHEVRON_ICON = (
    '<svg class="user-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    'aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
)


def decode_client_principal(raw: str | None) -> tuple[dict[str, Any] | None, str | None]:
    """Decode the base64 JSON payload of an x-ms-client-principal header.

    Returns (payload, error). Exactly one of the two is set when ``raw`` is present.
    """
    if not raw:
        return None, None
    normalized = raw.strip().replace("-", "+").replace("_", "/")
    normalized += "=" * (-len(normalized) % 4)
    try:
        decoded = base64.b64decode(normalized).decode("utf-8")
    except (binascii.Error, ValueError, UnicodeDecodeError) as exc:
        return None, f"Header is not valid base64-encoded UTF-8: {exc}"
    try:
        payload = json.loads(decoded)
    except json.JSONDecodeError as exc:
        return None, f"Decoded header is not valid JSON: {exc}"
    if not isinstance(payload, dict):
        return None, "Decoded header is not a JSON object."
    return payload, None


def _short_claim_type(claim_type: str) -> str:
    return claim_type.rsplit("/", 1)[-1] or claim_type


def _stat(label: str, value: object) -> str:
    text = "\u2014" if value in (None, "", []) else str(value)
    return (
        '<div class="stat">'
        f'<span class="stat-label">{escape(label)}</span>'
        f'<span class="stat-value">{escape(text)}</span>'
        "</div>"
    )


def _render_client_principal(raw: str | None) -> tuple[str, str, str]:
    """Return (badge text, badge tone, panel body HTML) for the decoded principal panel."""
    payload, error = decode_client_principal(raw)
    if raw is None:
        return (
            "Header not present",
            "",
            '<p class="empty">No <code>x-ms-client-principal</code> header was sent with this '
            "request.</p>",
        )
    if error is not None:
        return "Decode failed", "error", f'<p class="empty">{escape(error)}</p>'

    assert payload is not None
    claims_raw = payload.get("claims")
    claims = [c for c in claims_raw if isinstance(c, dict)] if isinstance(claims_raw, list) else []
    name_typ = payload.get("name_typ")
    role_typ = payload.get("role_typ")
    display_name = next(
        (str(c.get("val", "")) for c in claims if c.get("typ") == name_typ),
        None,
    )
    roles = [str(c.get("val", "")) for c in claims if c.get("typ") == role_typ]

    meta = "".join(
        (
            _stat("Auth type", payload.get("auth_typ")),
            _stat("Name", display_name),
            _stat("Roles", ", ".join(roles) if roles else None),
            _stat("Claims", len(claims)),
        )
    )

    if claims:
        claim_rows = "".join(
            '<tr><th scope="row" class="claim-type">'
            f"<span>{escape(_short_claim_type(str(claim.get('typ', ''))))}</span>"
            + (
                f"<small>{escape(str(claim.get('typ', '')))}</small>"
                if _short_claim_type(str(claim.get("typ", ""))) != str(claim.get("typ", ""))
                else ""
            )
            + f"</th><td>{escape(str(claim.get('val', '')))}</td></tr>"
            for claim in claims
        )
        claims_html = f'<div class="table-wrap"><table><tbody>{claim_rows}</tbody></table></div>'
    else:
        claims_html = '<p class="empty">Decoded payload contains no claims.</p>'

    raw_json = escape(json.dumps(payload, indent=2, sort_keys=True))
    body = (
        f'<div class="identity-meta">{meta}</div>'
        f"{claims_html}"
        '<details class="raw"><summary>View decoded JSON</summary>'
        f"<pre>{raw_json}</pre></details>"
    )
    return "Decoded", "success", body


def _cookie_entries(request: Request) -> list[tuple[str, str]]:
    """Return every Cookie header pair in browser order, preserving duplicate names."""
    entries: list[tuple[str, str]] = []
    for header_value in request.headers.getlist("cookie"):
        for raw_cookie in header_value.split(";"):
            name, separator, value = raw_cookie.partition("=")
            normalized_name = name.strip()
            if normalized_name:
                entries.append(
                    (normalized_name, value.strip() if separator else "")
                )
    return entries


def _render_table_value(value: str) -> str:
    encoded = escape(value)
    if len(value) <= _COLLAPSED_VALUE_LENGTH:
        return encoded
    return (
        '<details class="value-details">'
        f"<summary>Show value ({len(value)} characters)</summary>"
        f'<div class="long-value">{encoded}</div>'
        "</details>"
    )


def _render_request_inspector(request: Request) -> HTMLResponse:
    headers = sorted(request.headers.items(), key=lambda item: item[0].lower())
    cookies = _cookie_entries(request)
    easyauth_count = sum(
        name.lower().startswith(_EASYAUTH_HEADER_PREFIXES) for name, _ in headers
    )
    rows = "".join(
        f'<tr class="{"identity" if name.lower().startswith(_EASYAUTH_HEADER_PREFIXES) else ""}">'
        f'<th scope="row">{escape(name)}</th><td>{_render_table_value(value)}</td></tr>'
        for name, value in headers
    )
    cookie_rows = (
        "".join(
            f'<tr class="{"platform-cookie" if name.lower() in _PLATFORM_COOKIE_NAMES else ""}">'
            f'<th scope="row">{escape(name)}</th><td>{_render_table_value(value)}</td></tr>'
            for name, value in cookies
        )
        or '<tr><td colspan="2" class="empty">No cookies received.</td></tr>'
    )
    azure_socket_ip = request.headers.get("x-azure-socketip", "not present")
    principal_status, principal_tone, principal_body = _render_client_principal(
        request.headers.get("x-ms-client-principal")
    )
    identity_status = (
        f"{easyauth_count} EasyAuth-related header"
        f'{"s" if easyauth_count != 1 else ""} detected'
        if easyauth_count
        else "No EasyAuth-related headers detected"
    )
    identity_tone = "success" if easyauth_count else ""

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark">
  <title>EasyAuth Request Inspector / Builder Apps</title>
  <link rel="icon" type="image/svg+xml" href="{FAVICON}">
  {FONTS}
  <style>{STYLE}</style>
</head>
<body>
  <header class="topbar">
    <a href="/" class="brand">{LOGO}builder apps<span class="slash">/</span><span class="muted">easyauth inspector</span></a>
    <div class="topbar-end">
      <span class="tag">REQUEST INSPECTOR</span>
      <nav id="login-actions" class="login-actions" aria-label="Sign in options" hidden>
        <a class="button-secondary" href="/.auth/login/github">{_GITHUB_ICON}<span>GitHub</span></a>
        <a class="button-secondary" href="/.auth/login/entra">{_MICROSOFT_ICON}<span>Microsoft Entra</span></a>
      </nav>
      <div id="user" class="user" hidden>
        <button id="user-trigger" class="user-trigger" type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="auth-card">
          <span class="user-text"><span id="user-name" class="user-name"></span><span id="user-email" class="user-email" hidden></span></span>
          <span id="user-initials" class="avatar" aria-hidden="true"></span>
          {_CHEVRON_ICON}
        </button>
        <div id="auth-card" class="auth-card" role="dialog" aria-label="Signed-in account" hidden>
          <div class="auth-card-banner" aria-hidden="true"></div>
          <span id="card-initials" class="avatar avatar-lg" aria-hidden="true"></span>
          <div class="auth-card-body">
            <div id="card-name" class="auth-card-name"></div>
            <div id="card-login" class="auth-card-sub" hidden></div>
            <div id="card-email" class="auth-card-sub" hidden></div>
            <div class="auth-card-provider"><span class="dot" aria-hidden="true"></span><span id="card-provider"></span></div>
          </div>
          <div class="auth-card-foot">
            <a id="sign-out" class="auth-card-signout" href="/.auth/logout">{_SIGN_OUT_ICON}Sign out</a>
          </div>
        </div>
      </div>
    </div>
  </header>
  <main>
    <div class="hero">
      <section>
        <p class="eyebrow">Diagnostic app</p>
        <h1>EasyAuth<br><span class="muted">Request inspector</span></h1>
        <p class="lede">The complete request envelope delivered to the app, with injected identity headers highlighted.</p>
      </section>
      <section class="panel" aria-labelledby="request-title">
        <div class="panel-heading"><div><p class="eyebrow">Request</p><h2 id="request-title">What the app received.</h2></div></div>
        <dl class="config">
          <div><dt>Method</dt><dd>{escape(request.method)}</dd></div>
          <div><dt>Path</dt><dd>{escape(request.url.path)}</dd></div>
          <div><dt>X-Azure-SocketIP</dt><dd>{escape(azure_socket_ip)}</dd></div>
          <div><dt>Headers</dt><dd>{len(headers)}</dd></div>
        </dl>
      </section>
    </div>

    <section class="panel" aria-labelledby="principal-title">
      <div class="panel-heading">
        <div><p class="eyebrow">Header</p><h2 id="principal-title">Decoded <code>x-ms-client-principal</code></h2></div>
        <span class="badge {principal_tone}">{principal_status}</span>
      </div>
      <div class="panel-body">{principal_body}</div>
    </section>

    <section class="panel" id="auth-panel" aria-labelledby="auth-title">
      <div class="panel-heading">
        <div><p class="eyebrow">Endpoint</p><h2 id="auth-title">Identity <code>/.auth/me</code></h2></div>
        <span class="badge" id="auth-status">Loading&hellip;</span>
      </div>
      <div class="panel-body" id="auth-body">
        <p class="empty">Fetching <code>/.auth/me</code>&hellip;</p>
      </div>
    </section>

    <section class="panel" aria-labelledby="cookies-title">
      <div class="panel-heading">
        <div><p class="eyebrow">Cookies</p><h2 id="cookies-title">Cookies received by the app</h2></div>
        <span class="badge">{len(cookies)} cookie{"s" if len(cookies) != 1 else ""}</span>
      </div>
      <div class="table-wrap">
        <table>
          <tbody>{cookie_rows}</tbody>
        </table>
      </div>
    </section>

    <section class="panel" aria-labelledby="headers-title">
      <div class="panel-heading">
        <div><p class="eyebrow">Headers</p><h2 id="headers-title">Headers received by the app</h2></div>
        <span class="badge {identity_tone}">{identity_status}</span>
      </div>
      <div class="table-wrap">
        <table>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </section>

    <div class="footer">
      <span>Green rows match known EasyAuth or Embr identity header prefixes; red rows are platform cookies.</span>
      <a href="/headers">View raw JSON</a>
    </div>
  </main>
  <script>{SCRIPT}</script>
</body>
</html>"""
    return HTMLResponse(html)


@app.get("/", response_class=HTMLResponse)
def root(request: Request) -> HTMLResponse:
    return _render_request_inspector(request)


@app.get("/auth", response_class=HTMLResponse)
def auth_root(request: Request) -> HTMLResponse:
    return _render_request_inspector(request)


@app.get("/auth/cookies", response_class=HTMLResponse)
def auth_cookies(request: Request) -> HTMLResponse:
    return _render_request_inspector(request)


@app.api_route("/headers", methods=["GET", "POST", "PUT", "DELETE"])
def echo_headers(request: Request) -> JSONResponse:
    principal, principal_error = decode_client_principal(
        request.headers.get("x-ms-client-principal")
    )
    return JSONResponse(
        {
            "method": request.method,
            "path": request.url.path,
            "headers": dict(request.headers),
            "cookies": [
                {"name": name, "value": value}
                for name, value in _cookie_entries(request)
            ],
            "client": request.client.host if request.client else None,
            "client_principal": principal,
            "client_principal_error": principal_error,
        }
    )


@app.get("/health")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
