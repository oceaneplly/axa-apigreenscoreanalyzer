---
adr: 0008
title: Deploy runtime in ≥ 2 regions close to consumers (AR02)
status: accepted
date: 2026-07-02
green_rules: [AR02]
verifies:
  - kind: openapi_field
    path: servers
    expected_min_count: 2
  - kind: cdn_header_present
    headers: [cf-ray, x-amz-cf-id, x-azure-ref, x-served-by, x-akamai-request-id]
---

# 0008 — Multi-region runtime close to consumers

## Context

A single-region deployment forces cross-continent traffic for users on
the "wrong" side of the ocean. Latency goes up, energy per request goes
up, user-perceived quality goes down.

## Decision

Every production service MUST be deployed in **at least 2 regions**
matching its main consumer regions (declared via `--consumer-region`).
Traffic MUST be routed via a global edge / CDN (Cloudflare, CloudFront,
Front Door, Fastly, Akamai) so the TLS handshake is terminated close to
the user.

The OpenAPI spec MUST list the regional URLs under `servers[]`.

## Consequences

- P95 latency drops (typically −40 % to −70 % for cross-region users).
- **Verified in CI** by counting `servers[]` and detecting a CDN header
  on the base URL response.

