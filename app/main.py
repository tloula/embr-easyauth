# TEST-ONLY app: intentionally echoes all headers and must not run in production.

from __future__ import annotations

from html import escape

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="embr-easyauth", version="0.1.0")

_EASYAUTH_HEADER_PREFIXES = (
    "x-ms-client-principal",
    "x-ms-token-",
    "x-embr-",
    "x-adc-",
)


@app.get("/", response_class=HTMLResponse)
def root(request: Request) -> HTMLResponse:
    headers = sorted(request.headers.items(), key=lambda item: item[0].lower())
    easyauth_count = sum(
        name.lower().startswith(_EASYAUTH_HEADER_PREFIXES) for name, _ in headers
    )
    rows = "".join(
        f'<tr class="{"identity" if name.lower().startswith(_EASYAUTH_HEADER_PREFIXES) else ""}">'
        f'<th scope="row">{escape(name)}</th><td>{escape(value)}</td></tr>'
        for name, value in headers
    )
    azure_socket_ip = request.headers.get("x-azure-socketip", "not present")
    identity_status = (
        f"{easyauth_count} EasyAuth-related header"
        f'{"s" if easyauth_count != 1 else ""} detected'
        if easyauth_count
        else "No EasyAuth-related headers detected"
    )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>EasyAuth request inspector</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #14213d;
      --azure: #1677ff;
      --signal: #16855b;
      --paper: #f5f7fb;
      --line: #d9e2f0;
      --muted: #5d6b82;
      --white: #ffffff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        linear-gradient(135deg, rgb(22 119 255 / 8%), transparent 38rem),
        var(--paper);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    main {{ width: min(1120px, calc(100% - 32px)); margin: 0 auto; padding: 48px 0; }}
    .eyebrow {{
      color: var(--azure);
      font-size: 0.75rem;
      font-weight: 800;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }}
    h1 {{
      max-width: 760px;
      margin: 8px 0 12px;
      font-size: clamp(2rem, 5vw, 4rem);
      letter-spacing: -0.045em;
      line-height: 0.98;
    }}
    .intro {{ max-width: 720px; margin: 0; color: var(--muted); font-size: 1.05rem; }}
    .warning {{
      margin: 28px 0;
      border: 1px solid #efb43f;
      border-left-width: 5px;
      border-radius: 10px;
      background: #fff8e8;
      padding: 14px 18px;
      color: #704b00;
    }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin: 28px 0;
    }}
    .stat {{
      min-width: 0;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: rgb(255 255 255 / 82%);
      padding: 16px;
      box-shadow: 0 12px 32px rgb(20 33 61 / 6%);
    }}
    .stat-label {{
      display: block;
      margin-bottom: 5px;
      color: var(--muted);
      font-size: 0.7rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}
    .stat-value {{
      display: block;
      overflow-wrap: anywhere;
      font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace;
      font-size: 0.9rem;
      font-weight: 700;
    }}
    .panel {{
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: var(--white);
      box-shadow: 0 18px 50px rgb(20 33 61 / 8%);
    }}
    .panel-heading {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 18px 20px;
      border-bottom: 1px solid var(--line);
    }}
    .panel-heading h2 {{ margin: 0; font-size: 1rem; }}
    .status {{
      border-radius: 999px;
      background: {"#e9f8f1" if easyauth_count else "#eef2f8"};
      color: {"var(--signal)" if easyauth_count else "var(--muted)"};
      padding: 5px 10px;
      font-size: 0.75rem;
      font-weight: 800;
    }}
    .table-wrap {{ overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.84rem; }}
    th, td {{
      border-bottom: 1px solid var(--line);
      padding: 11px 20px;
      text-align: left;
      vertical-align: top;
      overflow-wrap: anywhere;
      font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace;
    }}
    th {{ width: 31%; color: var(--muted); font-weight: 700; }}
    tr:last-child th, tr:last-child td {{ border-bottom: 0; }}
    tr.identity {{ background: #effaf5; }}
    tr.identity th {{ color: var(--signal); }}
    .footer {{
      display: flex;
      justify-content: space-between;
      gap: 20px;
      margin-top: 14px;
      color: var(--muted);
      font-size: 0.8rem;
    }}
    a {{ color: var(--azure); font-weight: 700; }}
    @media (max-width: 760px) {{
      main {{ padding: 28px 0; }}
      .summary {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .panel-heading, .footer {{ align-items: flex-start; flex-direction: column; }}
      th, td {{ display: block; width: 100%; padding: 8px 14px; }}
      th {{ padding-bottom: 2px; border-bottom: 0; }}
      td {{ padding-top: 2px; }}
    }}
  </style>
</head>
<body>
  <main>
    <div class="eyebrow">Embr diagnostic app</div>
    <h1>EasyAuth request inspector</h1>
    <p class="intro">This page shows the complete request envelope delivered to the app. EasyAuth-related headers are highlighted so injected identity is easy to verify.</p>

    <div class="warning"><strong>Test only.</strong> Every header is displayed without redaction, including cookies and credentials. Do not deploy this app to production or expose it to real user traffic.</div>

    <section class="summary" aria-label="Request summary">
      <div class="stat"><span class="stat-label">Method</span><span class="stat-value">{escape(request.method)}</span></div>
      <div class="stat"><span class="stat-label">Path</span><span class="stat-value">{escape(request.url.path)}</span></div>
      <div class="stat"><span class="stat-label">X-Azure-SocketIP</span><span class="stat-value">{escape(azure_socket_ip)}</span></div>
      <div class="stat"><span class="stat-label">Headers</span><span class="stat-value">{len(headers)}</span></div>
    </section>

    <section class="panel">
      <div class="panel-heading">
        <h2>Headers received by the app</h2>
        <span class="status">{identity_status}</span>
      </div>
      <div class="table-wrap">
        <table>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </section>

    <div class="footer">
      <span>Green rows match known EasyAuth or Embr identity header prefixes.</span>
      <a href="/headers">View raw JSON</a>
    </div>
  </main>
</body>
</html>"""
    return HTMLResponse(html)


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
