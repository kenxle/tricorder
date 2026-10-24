"""The built page reaches tRPC through the same guarded Python origin."""

import httpx
from fastapi.testclient import TestClient

from server.app import app


def gateway(monkeypatch, handler):
    original = httpx.AsyncClient

    def client(**kwargs):
        assert kwargs["trust_env"] is False
        return original(transport=httpx.MockTransport(handler), **kwargs)

    monkeypatch.setattr("server.trpc_routes.httpx.AsyncClient", client)


def test_trpc_proxy_preserves_batch_query_status_and_json(monkeypatch):
    monkeypatch.setenv("TRICORDER_RPC_URL", "http://127.0.0.1:9876")
    query = 'batch=1&input=%7B%220%22%3A%7B%22json%22%3A%22hollis_voice%22%7D%7D'

    def upstream(request):
        assert str(request.url) == f"http://127.0.0.1:9876/trpc/room.readout?{query}"
        assert request.method == "GET"
        return httpx.Response(404, json=[{"error": {"message": "no readout yet"}}])

    gateway(monkeypatch, upstream)
    with TestClient(app, base_url="http://127.0.0.1") as web:
        response = web.get(f"/trpc/room.readout?{query}")
    assert response.status_code == 404
    assert response.json()[0]["error"]["message"] == "no readout yet"
    assert response.headers["cache-control"] == "no-store"


def test_trpc_unavailable_is_a_service_error(monkeypatch):
    def unavailable(request):
        raise httpx.ConnectError("connection refused", request=request)

    gateway(monkeypatch, unavailable)
    with TestClient(app, base_url="http://127.0.0.1") as web:
        response = web.get("/trpc/room.list")
    assert response.status_code == 503
    assert "gateway unavailable" in response.json()["detail"]


def test_trpc_guard_rejects_nonlocal_host_before_forwarding(monkeypatch):
    def unexpected(request):
        raise AssertionError("must not reach gateway")

    gateway(monkeypatch, unexpected)
    with TestClient(app, base_url="http://evil.example") as web:
        assert web.get("/trpc/room.list").status_code == 403


def test_trpc_does_not_forward_mutations(monkeypatch):
    def unexpected(request):
        raise AssertionError("must not reach gateway")

    gateway(monkeypatch, unexpected)
    with TestClient(app, base_url="http://127.0.0.1") as web:
        assert web.post("/trpc/room.list", json={}).status_code == 405
