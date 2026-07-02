---
adr: 0010
title: ADR gate — every architecture decision is verified in CI
status: accepted
date: 2026-07-02
green_rules: []
verifies: []
---

# 0010 — ADR gate: every architecture decision is verified in CI

## Context

ADRs traditionally sit unread in `docs/`. Without automated verification,
they slowly drift away from the running system.

## Decision

- Every ADR in `docs/adr/` MUST include a `verifies:` YAML block (may be
  empty for purely narrative ADRs).
- The analyzer runs `scripts/adr_rules.py` on every PR.
- An ADR with `status: accepted` and a failing verifier MUST fail the
  build (`--fail-on-adr-violation`).
- Deprecated or superseded ADRs are skipped by the verifier.

## Consequences

- No drift between documented architecture and running system.
- ADRs become **executable specifications**, not shelfware.
- **Verified in CI** by the analyzer itself — meta but necessary.

