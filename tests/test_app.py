from __future__ import annotations

import json
import unittest

from starlette.requests import Request

from app.main import _cookie_entries, app, auth_cookies, echo_headers, root


def make_request(
    path: str = "/",
    cookie_header: str | None = None,
    extra_headers: list[tuple[bytes, bytes]] | None = None,
) -> Request:
    headers = []
    if cookie_header is not None:
        headers.append((b"cookie", cookie_header.encode("latin-1")))
    if extra_headers is not None:
        headers.extend(extra_headers)
    return Request(
        {
            "type": "http",
            "http_version": "1.1",
            "method": "GET",
            "scheme": "https",
            "path": path,
            "raw_path": path.encode("latin-1"),
            "query_string": b"",
            "root_path": "",
            "headers": headers,
            "client": ("127.0.0.1", 12345),
            "server": ("example.test", 443),
        }
    )


class CookieInspectorTests(unittest.TestCase):
    def test_root_renders_all_parsed_cookies_and_escapes_values(self) -> None:
        response = root(make_request(cookie_header="session=abc123; theme=dark; unsafe=<b>"))
        body = response.body.decode()

        self.assertIn("Cookies received by the app", body)
        self.assertIn(">3 cookies<", body)
        self.assertIn("<th scope=\"row\">session</th><td>abc123</td>", body)
        self.assertIn("<th scope=\"row\">theme</th><td>dark</td>", body)
        self.assertIn("<th scope=\"row\">unsafe</th><td>&lt;b&gt;</td>", body)

    def test_root_reports_when_no_cookies_are_received(self) -> None:
        body = root(make_request()).body.decode()

        self.assertIn(">0 cookies<", body)
        self.assertIn("No cookies received.", body)

    def test_auth_cookies_renders_the_same_cookie_table(self) -> None:
        response = auth_cookies(
            make_request("/auth/cookies", "embr_refresh_token=secret; theme=dark")
        )
        body = response.body.decode()

        self.assertIn("Cookies received by the app", body)
        self.assertIn("<span class=\"stat-value\">/auth/cookies</span>", body)
        self.assertIn(
            '<tr class="platform-cookie"><th scope="row">embr_refresh_token</th><td>secret</td>',
            body,
        )
        self.assertIn("<th scope=\"row\">theme</th><td>dark</td>", body)

    def test_auth_routes_are_registered(self) -> None:
        paths = {route.path for route in app.routes}

        self.assertIn("/auth", paths)
        self.assertIn("/auth/cookies", paths)

    def test_headers_endpoint_includes_parsed_cookies(self) -> None:
        response = echo_headers(make_request(cookie_header="session=abc123; theme=dark"))
        payload = json.loads(response.body)

        self.assertEqual(
            [
                {"name": "session", "value": "abc123"},
                {"name": "theme", "value": "dark"},
            ],
            payload["cookies"],
        )

    def test_duplicate_cookie_names_are_preserved_in_browser_order(self) -> None:
        request = make_request(
            "/auth/cookies",
            "embr_refresh_token=AUTH_PATH_SECRET; "
            "embr_refresh_token=ROOT_PATH_VALUE; theme=dark",
        )

        self.assertEqual(
            [
                ("embr_refresh_token", "AUTH_PATH_SECRET"),
                ("embr_refresh_token", "ROOT_PATH_VALUE"),
                ("theme", "dark"),
            ],
            _cookie_entries(request),
        )

        body = auth_cookies(request).body.decode()
        self.assertIn(">3 cookies<", body)
        self.assertIn(
            '<tr class="platform-cookie"><th scope="row">embr_refresh_token</th><td>AUTH_PATH_SECRET</td>',
            body,
        )
        self.assertIn(
            '<tr class="platform-cookie"><th scope="row">embr_refresh_token</th><td>ROOT_PATH_VALUE</td>',
            body,
        )

    def test_platform_access_and_refresh_cookies_are_highlighted(self) -> None:
        body = root(
            make_request(
                cookie_header="embr_access_token=access; embr_refresh_token=refresh"
            )
        ).body.decode()

        self.assertEqual(2, body.count('class="platform-cookie"'))
        self.assertIn("tr.platform-cookie { background: #fff0f0; }", body)
        self.assertIn("tr.platform-cookie th { color: #b42318; }", body)

    def test_long_cookie_and_header_values_are_collapsed_by_default(self) -> None:
        long_value = "x" * 200
        body = root(
            make_request(
                cookie_header=f"embr_access_token={long_value}",
                extra_headers=[(b"x-long-diagnostic", long_value.encode("ascii"))],
            )
        ).body.decode()

        self.assertEqual(3, body.count('<details class="value-details">'))
        self.assertIn("Show value (200 characters)", body)
        self.assertIn("Show value (218 characters)", body)
        self.assertNotIn('<details class="value-details" open>', body)


if __name__ == "__main__":
    unittest.main()
