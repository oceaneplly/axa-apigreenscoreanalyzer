---
adr: 0007
title: Prefer events (SSE / AsyncAPI) over polling (AR01)
status: accepted
date: 2026-07-02
green_rules: [AR01, DE06]
verifies:
  - kind: sse_endpoint
    path: /**/events
    content_type: text/event-stream
  - kind: absent_query_param
    path: /**/changes
    param: poll
---

# 0007 — Prefer events over polling

## Context

Clients polling a `/changes` endpoint every N seconds waste round-trips
even when nothing changed. Push-based models (SSE, WebSocket, AsyncAPI)
divide the RTT/CPU cost by 10–100×.

## Decision

For every mutable resource, we MUST expose either:

1. A **Server-Sent Events** endpoint (`text/event-stream`) at `/events`
   or `/{resource}/events`; or
2. A documented **AsyncAPI** channel (Kafka / RabbitMQ / EventBridge /
   Service Bus) referenced from the OpenAPI `x-async-channel` extension.

Polling MAY remain as fallback (`/changes?since=<ts>`) but the client
docs MUST recommend the event channel first.

## Consequences

- Fewer round-trips, lower CPU, lower carbon per updated resource.
- **Verified in CI** via `sse_endpoint` cross-check (spec + runtime
  `Content-Type: text/event-stream`).

