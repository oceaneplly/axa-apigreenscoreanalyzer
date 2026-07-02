---
adr: 0004
title: Enable GZIP compression middleware (DE01)
status: accepted
date: 2026-07-02
green_rules: [DE01]
verifies:
  - kind: response_header_present
    path: /**
    header: Content-Encoding
    request_accept_encoding: gzip
---

# 0004 — Enable GZIP compression middleware

## Context

Text-based payloads (JSON) typically compress at 60–80 %. Not enabling
compression is a "free" win at the framework level.

## Decision

Every HTTP framework MUST enable a compression middleware at startup with
gzip **and** brotli (when the client advertises `Accept-Encoding: br`).
Threshold : compress responses ≥ 1 KB.

## Consequences

- ~70 % bandwidth reduction on JSON payloads.
- **Verified in CI** by probing with `Accept-Encoding: gzip` and asserting
  a `Content-Encoding: gzip` response header.

## Framework snippets

- **Spring Boot**: `server.compression.enabled=true`
- **FastAPI**: `app.add_middleware(GZipMiddleware, minimum_size=1024)`
- **ASP.NET Core**: `services.AddResponseCompression()`

