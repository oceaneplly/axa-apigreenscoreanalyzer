---
adr: 0003
title: ETag caching strategy on GET single-resource (DE02/DE03)
status: accepted
date: 2026-07-02
green_rules: [DE02, DE03]
verifies:
  - kind: response_header_present
    path: /**
    header: ETag
  - kind: endpoint_returns_status
    path: /**
    status: 304
---

# 0003 — ETag caching strategy on GET single-resource

## Context

Repeated `GET` on the same resource wastes bandwidth if the payload has
not changed. Weak/strong `ETag` + `304 Not Modified` cut the payload to
zero on cache hits.

## Decision

Every `GET` on a single resource MUST return a `ETag` header (weak
validator based on the resource's `updatedAt`). The server MUST honour
`If-None-Match` and respond `304 Not Modified` when the ETag matches.

## Consequences

- Cache hits transfer 0 body bytes.
- **Verified in CI** by probing `If-None-Match` and checking runtime
  `ETag` header presence.

