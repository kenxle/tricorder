"""Same-origin entry point for the read-only TypeScript tRPC gateway."""

import os

import httpx
from fastapi import APIRouter, HTTPException, Request, Response

router = APIRouter()


@router.get("/trpc/{procedure:path}")
async def trpc_query(procedure: str, request: Request) -> Response:
    # The destination is operator configuration, never supplied by a request.
    upstream = os.environ.get("TRICORDER_RPC_URL") or "http://127.0.0.1:8789"
    url = f"{upstream.rstrip('/')}/trpc/{procedure}"
    if request.url.query:
        url += f"?{request.url.query}"
    try:
        async with httpx.AsyncClient(timeout=30, trust_env=False) as client:
            result = await client.get(url, follow_redirects=False)
    except httpx.RequestError as exc:
        raise HTTPException(503, "tRPC gateway unavailable. Start it with pnpm dev or bin/serve.") from exc
    # httpx decodes response bodies, so do not copy encoding or length headers.
    return Response(result.content, status_code=result.status_code,
                    headers={"content-type": result.headers.get("content-type", "application/json"),
                             "cache-control": "no-store"})
