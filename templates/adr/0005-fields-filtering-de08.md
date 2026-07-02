---
adr: 0005
title: Field-filtering via ?fields query param (DE08)
status: accepted
date: 2026-07-02
green_rules: [DE08]
verifies:
  - kind: has_pagination_params
    path: /**
    params: [fields]
    any_of: true
---

# 0005 — Field-filtering via `?fields` query param

## Context

Clients often need only a subset of a resource (e.g. mobile lists show
`id + title` while desktop shows the full object). Sending the full
payload wastes bandwidth and battery on the client.

## Decision

Every `GET` endpoint MUST support a `?fields=<csv>` query param that
restricts the JSON response to the requested keys. Nested fields use
dot-notation: `?fields=id,author.name`.

## Consequences

- Payload reduction ranging from 30 % (few fields dropped) to 90 %
  (mobile list use-case).
- **Verified in CI** via `has_pagination_params` checker in "params
  presence" mode.

