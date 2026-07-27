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
    .panel + .panel {{ margin-top: 24px; }}
    .panel-body {{ padding: 18px 20px; }}
    .identity-card + .identity-card {{ margin-top: 18px; border-top: 1px solid var(--line); padding-top: 18px; }}
    .identity-meta {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }}
    .claim-type {{ color: var(--muted); font-weight: 700; }}
    .claim-type small {{ display: block; font-weight: 400; font-size: 0.72rem; opacity: 0.75; }}
    .empty {{ margin: 0; color: var(--muted); }}
    details.raw {{ margin-top: 16px; }}
    details.raw summary {{ cursor: pointer; color: var(--azure); font-weight: 700; font-size: 0.8rem; }}
    details.raw pre {{
      overflow-x: auto;
      margin: 10px 0 0;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: var(--paper);
      padding: 12px 14px;
      font-size: 0.78rem;
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
    <p class="intro">This page shows the complete request envelope delivered to the app. EasyAuth-related headers are highlighted so injected identity is easy to verify, and the browser calls <code>/.auth/me</code> to render the signed-in principal and its claims.</p>

    <section class="summary" aria-label="Request summary">
      <div class="stat"><span class="stat-label">Method</span><span class="stat-value">{escape(request.method)}</span></div>
      <div class="stat"><span class="stat-label">Path</span><span class="stat-value">{escape(request.url.path)}</span></div>
      <div class="stat"><span class="stat-label">X-Azure-SocketIP</span><span class="stat-value">{escape(azure_socket_ip)}</span></div>
      <div class="stat"><span class="stat-label">Headers</span><span class="stat-value">{len(headers)}</span></div>
    </section>

    <section class="panel" id="auth-panel">
      <div class="panel-heading">
        <h2>EasyAuth identity (<code>/.auth/me</code>)</h2>
        <span class="status" id="auth-status">Loading&hellip;</span>
      </div>
      <div class="panel-body" id="auth-body">
        <p class="empty">Fetching <code>/.auth/me</code>&hellip;</p>
      </div>
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
  <script>
  (function () {{
    var statusEl = document.getElementById('auth-status');
    var bodyEl = document.getElementById('auth-body');

    function el(tag, text) {{
      var node = document.createElement(tag);
      if (text !== undefined && text !== null) {{ node.textContent = String(text); }}
      return node;
    }}

    function setStatus(text) {{ statusEl.textContent = text; }}

    function shortClaim(type) {{
      var parts = String(type).split('/');
      return parts[parts.length - 1] || type;
    }}

    function stat(label, value) {{
      var wrap = el('div');
      wrap.className = 'stat';
      var l = el('span', label);
      l.className = 'stat-label';
      var v = el('span', value === undefined || value === null || value === '' ? '—' : value);
      v.className = 'stat-value';
      wrap.appendChild(l);
      wrap.appendChild(v);
      return wrap;
    }}

    function claimsTable(claims) {{
      var wrap = el('div');
      wrap.className = 'table-wrap';
      var table = el('table');
      var tbody = el('tbody');
      claims.forEach(function (claim) {{
        var tr = el('tr');
        var th = el('th');
        th.className = 'claim-type';
        th.setAttribute('scope', 'row');
        th.appendChild(el('span', shortClaim(claim.typ)));
        if (shortClaim(claim.typ) !== claim.typ) {{ th.appendChild(el('small', claim.typ)); }}
        tr.appendChild(th);
        tr.appendChild(el('td', claim.val));
        tbody.appendChild(tr);
      }});
      table.appendChild(tbody);
      wrap.appendChild(table);
      return wrap;
    }}

    function render(identities) {{
      bodyEl.textContent = '';
      if (!Array.isArray(identities) || identities.length === 0) {{
        setStatus('Not authenticated');
        var none = el('p', 'No identity returned by /.auth/me.');
        none.className = 'empty';
        bodyEl.appendChild(none);
        return;
      }}
      setStatus(identities.length + ' identit' + (identities.length === 1 ? 'y' : 'ies'));
      identities.forEach(function (identity) {{
        var card = el('section');
        card.className = 'identity-card';
        var meta = el('div');
        meta.className = 'identity-meta';
        meta.appendChild(stat('Provider', identity.provider_name));
        meta.appendChild(stat('User ID', identity.user_id));
        if (identity.expires_on) {{ meta.appendChild(stat('Expires on', identity.expires_on)); }}
        var claims = identity.user_claims || [];
        meta.appendChild(stat('Claims', claims.length));
        card.appendChild(meta);
        if (claims.length) {{
          card.appendChild(claimsTable(claims));
        }} else {{
          var none = el('p', 'No claims present.');
          none.className = 'empty';
          card.appendChild(none);
        }}
        bodyEl.appendChild(card);
      }});

      var raw = el('details');
      raw.className = 'raw';
      raw.appendChild(el('summary', 'View raw /.auth/me JSON'));
      raw.appendChild(el('pre', JSON.stringify(identities, null, 2)));
      bodyEl.appendChild(raw);
    }}

    function fail(message, showLogin) {{
      setStatus('Unavailable');
      bodyEl.textContent = '';
      var p = el('p', message);
      p.className = 'empty';
      bodyEl.appendChild(p);
      if (showLogin) {{
        var link = el('a', 'Sign in with /.auth/login/aad');
        link.href = '/.auth/login/aad';
        bodyEl.appendChild(link);
      }}
    }}

    fetch('/.auth/me', {{ credentials: 'include', headers: {{ Accept: 'application/json' }} }})
      .then(function (response) {{
        if (response.status === 401 || response.status === 403) {{
          fail('Not authenticated (HTTP ' + response.status + ').', true);
          return null;
        }}
        if (!response.ok) {{
          fail('/.auth/me returned HTTP ' + response.status + '. EasyAuth may not be enabled for this app.', false);
          return null;
        }}
        return response.json();
      }})
      .then(function (data) {{
        if (data === null) {{ return; }}
        render(data);
      }})
      .catch(function (error) {{
        fail('Failed to fetch /.auth/me: ' + error.message, false);
      }});
  }})();
  </script>
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
