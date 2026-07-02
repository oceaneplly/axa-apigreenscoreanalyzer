"""Sample FastAPI app for the Green Score workshop.

BASELINE (intentional): no pagination, no gzip middleware, no ETag,
/items/events returns a JSON list instead of SSE. Participants improve
these during Act 2 & 3.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, Response

app = FastAPI(
    title="Green API workshop — Python sample",
    version="0.1.0",
)

_ITEMS: list[dict[str, Any]] = [
    {
        "id": i,
        "title": f"Item #{i}",
        "description": "Long description body " * 20,
        "updatedAt": datetime.now(timezone.utc).isoformat(),
    }
    for i in range(1, 201)
]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "UP"}


# ❌ DE11: no pagination.
@app.get("/items")
def list_items() -> list[dict[str, Any]]:
    return _ITEMS


# ❌ DE02/03: no ETag support.
@app.get("/items/{item_id}")
def get_item(item_id: int) -> dict[str, Any]:
    for it in _ITEMS:
        if it["id"] == item_id:
            return it
    return Response(status_code=404)  # type: ignore[return-value]


# ❌ AR01: polling-style — should become SSE (StreamingResponse
#           with media_type="text/event-stream").
@app.get("/items/events")
def events() -> list[dict[str, Any]]:
    return _ITEMS[:5]


# ✅ DE06 baseline: delta sync via ?since=
@app.get("/items/changes")
def changes(since: int | None = None) -> list[dict[str, Any]]:
    return _ITEMS[:3]


@app.post("/items")
def create(body: dict[str, Any]) -> dict[str, Any]:
    body["id"] = len(_ITEMS) + 1
    return body

