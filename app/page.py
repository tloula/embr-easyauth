"""Shared assets (logo, CSS, JS) for the request inspector page.

They are inlined into the HTML response so the page is self-contained for both the container and
Azure Functions flavours.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

_SVG = (Path(__file__).parent / "builder-apps.svg").read_text(encoding="utf-8")

LOGO = re.sub(
    r'width="18" height="18"',
    'class="brand-logo" width="24" height="24" aria-hidden="true"',
    _SVG,
    count=1,
)
FAVICON = "data:image/svg+xml," + quote(_SVG)

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700'
    '&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">'
)

STYLE = """
:root {
  color-scheme: dark;
  --bg: #000;
  --panel: #0a0a0a;
  --border: #262626;
  --text: #ededed;
  --muted: #a1a1a1;
  --green: #74d6a0;
  --red: #ff9292;
  --sans: "Geist", system-ui, sans-serif;
  --mono: "Geist Mono", ui-monospace, Consolas, monospace;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text); font: 14px/1.6 var(--sans); -webkit-font-smoothing: antialiased; }
a { color: inherit; text-decoration: none; }
code { font: 12px var(--mono); }
.topbar { min-height: 76px; border-bottom: 1px solid var(--border); padding: 20px 5vw; display: flex; align-items: center; justify-content: space-between; gap: 20px; }
.brand { display: inline-flex; align-items: center; font-weight: 600; }
.brand-logo { flex-shrink: 0; margin-right: 10px; }
.slash { margin: 0 16px; color: #666; font-weight: 400; }
.muted { color: var(--muted); }
.tag, .eyebrow { font: 11px/1.5 var(--mono); letter-spacing: .09em; color: var(--muted); }
.tag { border: 1px solid var(--border); border-radius: 5px; padding: 5px 10px; }
.topbar-end { display: flex; align-items: center; gap: 14px; min-width: 0; }
main { width: min(1120px, calc(100% - 64px)); margin: 0 auto; padding: 88px 0 48px; display: grid; gap: 28px; }
.hero { display: grid; grid-template-columns: .85fr 1.15fr; gap: 64px; align-items: start; margin-bottom: 36px; }
.eyebrow { margin: 0 0 16px; text-transform: uppercase; }
h1 { font-size: clamp(48px, 5.8vw, 76px); font-weight: 500; letter-spacing: -.065em; line-height: 1.06; margin: 0 0 28px; }
.lede { font-size: 16px; color: var(--muted); max-width: 360px; margin: 0; }
.panel { border: 1px solid var(--border); border-radius: 12px; background: var(--panel); padding: 28px; min-width: 0; }
.panel-heading { display: flex; justify-content: space-between; align-items: center; gap: 16px; }
.panel-heading .eyebrow { margin-bottom: 7px; }
h2 { margin: 0; font-weight: 500; font-size: 21px; letter-spacing: -.025em; }
.badge { white-space: nowrap; border: 1px solid var(--border); border-radius: 20px; padding: 4px 9px; font: 11px/1.5 var(--mono); color: var(--muted); }
.badge.success { color: var(--green); border-color: #28583b; }
.badge.error { color: var(--red); border-color: #693838; }
.config { margin: 25px 0 0; border-top: 1px solid var(--border); padding-top: 18px; }
.config div { display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 5px 0; }
dt { color: var(--muted); }
dd { margin: 0; font: 12px/1.8 var(--mono); text-align: right; overflow-wrap: anywhere; }
.panel-body { margin-top: 25px; border-top: 1px solid var(--border); padding-top: 18px; }
.identity-card + .identity-card { margin-top: 22px; border-top: 1px solid var(--border); padding-top: 22px; }
.identity-meta { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 18px; }
.stat { min-width: 0; border: 1px solid var(--border); border-radius: 8px; background: var(--bg); padding: 12px 14px; }
.stat-label { display: block; margin-bottom: 2px; font: 11px/1.5 var(--mono); letter-spacing: .09em; text-transform: uppercase; color: var(--muted); }
.stat-value { display: block; overflow-wrap: anywhere; font: 12px/1.8 var(--mono); }
.empty { margin: 0; color: var(--muted); font-size: 12px; }
.table-wrap { overflow-x: auto; margin-top: 25px; border-top: 1px solid var(--border); }
.panel-body .table-wrap { margin-top: 0; border-top: 0; }
table { width: 100%; border-collapse: collapse; font: 12px/1.7 var(--mono); }
th, td { border-bottom: 1px solid var(--border); padding: 10px 14px 10px 0; text-align: left; vertical-align: top; overflow-wrap: anywhere; }
th { width: 31%; color: var(--muted); font-weight: 500; }
tr:last-child th, tr:last-child td { border-bottom: 0; }
tr.identity { background: #0c1911; }
tr.identity th, tr.identity td { padding-left: 12px; }
tr.identity th { color: var(--green); }
tr.platform-cookie { background: #211111; }
tr.platform-cookie th, tr.platform-cookie td { padding-left: 12px; }
tr.platform-cookie th { color: var(--red); }
.claim-type small { display: block; font-weight: 400; font-size: 11px; opacity: .7; }
details summary { cursor: pointer; color: var(--muted); font: 500 12px var(--sans); }
details summary:hover { color: var(--text); }
details.raw { margin-top: 18px; }
pre { margin: 10px 0 0; padding: 14px; border: 1px solid var(--border); border-radius: 6px; background: var(--bg); font: 11px/1.7 var(--mono); white-space: pre-wrap; overflow-wrap: anywhere; }
.long-value { margin-top: 8px; overflow-wrap: anywhere; }
.footer { display: flex; justify-content: space-between; gap: 20px; color: var(--muted); font-size: 12px; }
.footer a { color: var(--text); text-decoration: underline; text-underline-offset: 3px; text-decoration-color: var(--border); }
.footer a:hover { text-decoration-color: var(--muted); }
button { font: 500 13px/1.5 var(--sans); cursor: pointer; }
.button-secondary { display: inline-flex; align-items: center; gap: 8px; min-height: 36px; padding: 7px 12px; border: 1px solid var(--border); border-radius: 6px; color: var(--text); font-size: 13px; font-weight: 500; white-space: nowrap; }
.button-secondary:hover { background: #111; border-color: #3a3a3a; }
.button-secondary svg { width: 16px; height: 16px; flex: none; }
.login-actions { display: flex; gap: 10px; }
:focus-visible { outline: 2px solid var(--text); outline-offset: 5px; }
[hidden] { display: none !important; }
.user { position: relative; display: flex; align-items: center; min-width: 0; }
.user-trigger { display: flex; align-items: center; gap: 10px; min-width: 0; color: var(--text); background: none; border: 1px solid transparent; border-radius: 999px; padding: 3px 6px 3px 12px; font-weight: 400; transition: background .15s, border-color .15s; }
.user-trigger:hover, .user-trigger[aria-expanded="true"] { background: #111; border-color: var(--border); }
.user-trigger:focus-visible { outline-offset: 2px; }
.user-chevron { color: #666; flex: none; transition: transform .2s; }
.user-trigger[aria-expanded="true"] .user-chevron { transform: rotate(180deg); }
.avatar { width: 28px; height: 28px; border-radius: 50%; display: grid; place-items: center; font-size: 11px; font-weight: 600; color: #fff; background: linear-gradient(90deg, #3bd5ff, #367af2 50%, #8b52f4); flex: none; }
.user-text { display: flex; flex-direction: column; line-height: 1.2; min-width: 0; text-align: right; }
.user-name { font-size: 13px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-email { font-size: 12px; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.auth-card { position: absolute; top: calc(100% + 10px); right: 0; z-index: 50; width: 300px; max-width: calc(100vw - 32px); background: var(--panel); border: 1px solid #2e2e2e; border-radius: 14px; overflow: hidden; box-shadow: 0 24px 48px -12px rgba(0, 0, 0, .8); transform-origin: top right; animation: auth-card-in .18s cubic-bezier(.2, .8, .2, 1); }
@keyframes auth-card-in { from { opacity: 0; transform: translateY(-4px) scale(.97); } }
.auth-card-banner { height: 56px; position: relative; background: radial-gradient(80% 140% at 0% 0%, rgba(76, 141, 255, .14), transparent 70%), radial-gradient(60% 120% at 100% 0%, rgba(139, 82, 244, .1), transparent 70%), #111; border-bottom: 1px solid var(--border); }
.auth-card-banner::before { content: ""; position: absolute; inset: 0 0 auto; height: 1px; background: linear-gradient(90deg, #3bd5ff, #367af2 50%, #8b52f4); opacity: .6; }
.avatar-lg { width: 52px; height: 52px; font-size: 18px; margin: -26px 0 0 18px; position: relative; box-shadow: 0 0 0 4px var(--panel), 0 0 0 5px var(--border); }
.auth-card-body { padding: 10px 18px 16px; display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.auth-card-name { font-size: 16px; font-weight: 600; letter-spacing: -.01em; overflow-wrap: anywhere; }
.auth-card-sub { font-size: 13px; color: var(--muted); overflow-wrap: anywhere; }
.auth-card-provider { display: inline-flex; align-items: center; gap: 7px; align-self: flex-start; margin-top: 10px; font-size: 11.5px; color: var(--muted); border: 1px solid var(--border); background: var(--bg); border-radius: 999px; padding: 3px 10px 3px 8px; }
.auth-card-provider .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--green); box-shadow: 0 0 0 3px rgba(116, 214, 160, .15); }
.auth-card-foot { border-top: 1px solid var(--border); padding: 12px 18px; }
.auth-card-signout { display: flex; align-items: center; justify-content: center; gap: 8px; height: 34px; border-radius: 8px; font-size: 13px; font-weight: 500; color: #000; background: var(--text); transition: background .15s; }
.auth-card-signout:hover { background: #fff; }
.auth-card-signout:focus-visible { outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) { .auth-card { animation: none; } .user-chevron, .user-trigger { transition: none; } }
@media (max-width: 850px) {
  main { width: min(580px, calc(100% - 32px)); padding-top: 48px; }
  .hero { grid-template-columns: 1fr; gap: 36px; margin-bottom: 8px; }
  h1 { font-size: 56px; }
  .lede { max-width: 440px; }
  .tag, .user-text, .button-secondary span { display: none; }
  .footer { flex-direction: column; gap: 8px; }
}
@media (max-width: 600px) {
  .panel { padding: 18px; }
  .panel-heading { align-items: start; flex-direction: column; gap: 10px; }
  th, td { display: block; width: 100%; }
  th { padding-bottom: 0; border-bottom: 0; }
  td { padding-top: 0; }
  tr.identity th, tr.identity td, tr.platform-cookie th, tr.platform-cookie td { padding-left: 12px; padding-right: 12px; }
}
"""

SCRIPT = """
(() => {
  const NAME = "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name";
  const EMAIL = "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress";
  const PROVIDERS = { github: "GitHub", aad: "Microsoft Entra ID", entra: "Microsoft Entra ID" };
  const $ = (id) => document.getElementById(id);
  const statusEl = $("auth-status");
  const bodyEl = $("auth-body");
  const loginActions = $("login-actions");
  const userRoot = $("user");
  const trigger = $("user-trigger");
  const card = $("auth-card");

  function el(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined && text !== null) node.textContent = String(text);
    if (className) node.className = className;
    return node;
  }

  function setStatus(text, tone) {
    statusEl.textContent = text;
    statusEl.className = tone ? `badge ${tone}` : "badge";
  }

  function setText(id, value) {
    $(id).textContent = value ?? "";
    $(id).hidden = !value;
  }

  const shortClaim = (type) => String(type).split("/").pop() || type;

  function stat(label, value) {
    const wrap = el("div", null, "stat");
    wrap.append(el("span", label, "stat-label"), el("span", value === undefined || value === null || value === "" ? "\\u2014" : value, "stat-value"));
    return wrap;
  }

  function claimsTable(claims) {
    const wrap = el("div", null, "table-wrap");
    const tbody = el("tbody");
    claims.forEach((claim) => {
      const row = el("tr");
      const th = el("th", null, "claim-type");
      th.scope = "row";
      th.append(el("span", shortClaim(claim.typ)));
      if (shortClaim(claim.typ) !== claim.typ) th.append(el("small", claim.typ));
      row.append(th, el("td", claim.val));
      tbody.append(row);
    });
    const table = el("table");
    table.append(tbody);
    wrap.append(table);
    return wrap;
  }

  function toUser(identity) {
    const claim = (typ) => identity.user_claims?.find((c) => c.typ === typ)?.val;
    const email = claim(EMAIL) ?? claim("preferred_username");
    const login = claim("urn:github:login");
    const name = claim("name") ?? claim(NAME) ?? claim("urn:github:name") ?? login ?? email ?? identity.user_id;
    if (!name) return null;
    return {
      name,
      email: email !== name ? email : undefined,
      login: login !== name ? login : undefined,
      provider: PROVIDERS[identity.provider_name] ?? identity.provider_name,
    };
  }

  function renderUser(user) {
    const initials = user.name.split(/[\\s@._-]+/).filter(Boolean).slice(0, 2)
      .map((part) => part[0].toUpperCase()).join("");
    $("user-initials").textContent = initials;
    $("card-initials").textContent = initials;
    $("user-name").textContent = user.name;
    $("card-name").textContent = user.name;
    setText("user-email", user.email);
    setText("card-email", user.email);
    setText("card-login", user.login && `@${user.login}`);
    $("card-provider").textContent = `Signed in with ${user.provider} via EasyAuth`;
    userRoot.hidden = false;
  }

  function showAuthActions(isAuthenticated) {
    loginActions.hidden = isAuthenticated;
    if (!isAuthenticated) userRoot.hidden = true;
  }

  function render(identities) {
    bodyEl.textContent = "";
    if (!Array.isArray(identities) || identities.length === 0) {
      setStatus("Not authenticated");
      showAuthActions(false);
      bodyEl.append(el("p", "No identity returned by /.auth/me.", "empty"));
      return;
    }
    showAuthActions(true);
    const user = toUser(identities[0]);
    if (user) renderUser(user);
    setStatus(`${identities.length} identit${identities.length === 1 ? "y" : "ies"}`, "success");
    identities.forEach((identity) => {
      const section = el("section", null, "identity-card");
      const meta = el("div", null, "identity-meta");
      const claims = identity.user_claims || [];
      meta.append(stat("Provider", identity.provider_name), stat("User ID", identity.user_id));
      if (identity.expires_on) meta.append(stat("Expires on", identity.expires_on));
      meta.append(stat("Claims", claims.length));
      section.append(meta);
      section.append(claims.length ? claimsTable(claims) : el("p", "No claims present.", "empty"));
      bodyEl.append(section);
    });
    const raw = el("details", null, "raw");
    raw.append(el("summary", "View raw /.auth/me JSON"), el("pre", JSON.stringify(identities, null, 2)));
    bodyEl.append(raw);
  }

  function fail(message, isLoggedOut) {
    setStatus("Unavailable", "error");
    bodyEl.textContent = "";
    bodyEl.append(el("p", message, "empty"));
    if (isLoggedOut) showAuthActions(false);
  }

  function setOpen(open, restoreFocus = false) {
    card.hidden = !open;
    trigger.setAttribute("aria-expanded", String(open));
    if (open) $("sign-out").focus();
    else if (restoreFocus) trigger.focus();
  }

  trigger.addEventListener("click", () => setOpen(card.hidden));
  document.addEventListener("pointerdown", (event) => {
    if (!card.hidden && !userRoot.contains(event.target)) setOpen(false);
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !card.hidden) setOpen(false, true);
  });
  userRoot.addEventListener("focusout", (event) => {
    if (!card.hidden && !userRoot.contains(event.relatedTarget)) setOpen(false);
  });

  fetch("/.auth/me", { credentials: "include", headers: { Accept: "application/json" } })
    .then((response) => {
      if (response.status === 401 || response.status === 403) {
        fail(`Not authenticated (HTTP ${response.status}).`, true);
        return null;
      }
      if (!response.ok) {
        fail(`/.auth/me returned HTTP ${response.status}. EasyAuth may not be enabled for this app.`, false);
        return null;
      }
      return response.json();
    })
    .then((data) => { if (data !== null) render(data); })
    .catch((error) => fail(`Failed to fetch /.auth/me: ${error.message}`, false));
})();
"""
