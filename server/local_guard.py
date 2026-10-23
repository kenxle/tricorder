"""The server answers only its own page on this machine.

Tricorder binds to localhost, but a website the operator visits can still reach it:
a cross-site form or no-cors fetch can POST to any route, and a DNS-rebinding name can
point at 127.0.0.1 and read the answers. This middleware refuses, before any route runs:

- a request whose Host is not localhost, 127.0.0.1 or [::1] (any port): DNS rebinding;
- a POST, PUT, PATCH or DELETE whose Origin (or Referer, when Origin is absent) is present
  and is not a loopback origin (any port, so the Vite dev server on :5173 still works);
- a POST, PUT, PATCH or DELETE that carries a body without a JSON, octet-stream or
  multipart content type. text/plain and form bodies are what a cross-site form can send
  without a preflight. A write with no body (rebuild the readout) needs no content type.

A plain ASGI middleware, so a streamed upload is never buffered here.
Review: docs/features/20261022.10_feature_breakdown/review_wave2a.md, S1.
"""

from __future__ import annotations

import json
from urllib.parse import urlsplit

LOOPBACK = {"localhost", "127.0.0.1", "::1"}
UNSAFE = {"POST", "PUT", "PATCH", "DELETE"}
BODY_TYPES = ("application/json", "application/octet-stream", "multipart/form-data")


def _hostname(netloc: str) -> str | None:
    """'127.0.0.1:8812' to '127.0.0.1', '[::1]:80' to '::1'; None when it is not a host."""
    try:
        parts = urlsplit("//" + netloc)
        parts.port  # noqa: B018 - raises on a bad port
        return parts.hostname
    except ValueError:
        return None


def local_host(value: str) -> bool:
    return bool(value) and _hostname(value) in LOOPBACK


def local_origin(value: str) -> bool:
    """An http(s) origin or URL on a loopback host, any port. 'null' is not local."""
    try:
        parts = urlsplit(value)
    except ValueError:
        return False
    return parts.scheme in ("http", "https") and parts.netloc != "" and local_host(parts.netloc)


class LocalGuard:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = {k.decode("latin-1").lower(): v.decode("latin-1") for k, v in scope["headers"]}
        refusal = self.refuse(scope["method"].upper(), headers)
        if refusal is None:
            return await self.app(scope, receive, send)
        status, message = refusal
        body = json.dumps({"detail": message}).encode()
        await send({"type": "http.response.start", "status": status,
                    "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(body)).encode())]})
        await send({"type": "http.response.body", "body": body})

    @staticmethod
    def refuse(method: str, headers: dict[str, str]) -> tuple[int, str] | None:
        if not local_host(headers.get("host", "")):
            return 403, "This server answers only on localhost: the request's host is not this machine."
        if method not in UNSAFE:
            return None
        origin = headers.get("origin") or headers.get("referer")
        if origin is not None and not local_origin(origin):
            return 403, "Refused: this request came from another site."
        ctype = headers.get("content-type", "").split(";")[0].strip().lower()
        has_body = headers.get("content-length", "0") not in ("", "0") or "transfer-encoding" in headers
        if ctype or has_body:
            if ctype not in BODY_TYPES:
                return 415, "Send JSON (or the raw file as application/octet-stream)."
        return None
