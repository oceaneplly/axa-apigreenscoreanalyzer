---
adr: 0002
title: Mandatory pagination on collection endpoints (DE11)
status: accepted
date: 2026-07-02
green_rules: [DE11]
verifies:
  - kind: has_pagination_params
    path: /**
    params: [page, size]
  - kind: has_pagination_params
    path: /**
    params: [limit, offset]
    any_of: true
---

# 0002 — Mandatory pagination on collection endpoints

## Context

Endpoints returning collections (`GET /items`, `GET /users`…) can return
arbitrarily large payloads. Without pagination, network usage and client
memory grow linearly with data.

## Decision

Every collection endpoint MUST support either `page` + `size` (default) or
`limit` + `offset` query parameters. Default `size = 20`, max `size = 100`.

## Consequences

- Bandwidth reduction on typical clients.
- Predictable server memory footprint.
- **Verified in CI** via `has_pagination_params` on `/**` collection
  routes.

## Rejected alternatives

- **Cursor-based only** — great for infinite scroll but harder for admin
  UIs that need jump-to-page. May be introduced later per-service.

