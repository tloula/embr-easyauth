from __future__ import annotations

import json
import unittest

from starlette.requests import Request

from app.main import echo_headers, root


def make_request(cookie_header: str | None = None) -> Request:
    headers = []
    if cookie_header is not None:
        headers.append((b"cookie", cookie_header.encode("latin-1")))
    return Request(
        {
            "type": "http",
            "http_version": "1.1",
            "method": "GET",
            "scheme": "https",
            "path": "/",
            "raw_path": b"/",
            "query_string": b"",
            "root_path": "",
            "headers": headers,
            "client": ("127.0.0.1", 12345),
            "server": ("example.test", 443),
        }
    )


class CookieInspectorTests(unittest.TestCase):
    def test_root_renders_all_parsed_cookies_and_escapes_values(self) -> None:
        response = root(make_request("session=abc123; theme=dark; unsafe=<b>"))
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

    def test_headers_endpoint_includes_parsed_cookies(self) -> None:
        response = echo_headers(make_request("session=abc123; theme=dark"))
        payload = json.loads(response.body)

        self.assertEqual(
            {"session": "abc123", "theme": "dark"},
            payload["cookies"],
        )


if __name__ == "__main__":
    unittest.main()
