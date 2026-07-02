---
adr: 0006
title: Expose /health and /metrics observability endpoints (LO01)
status: accepted
date: 2026-07-02
green_rules: [LO01, AR05]
verifies:
  - kind: has_health_endpoint
    paths: [/health, /actuator/health, /metrics, /actuator/prometheus, /q/metrics]
---

# 0006 — Expose /health and /metrics observability endpoints

## Context

Without health and metrics endpoints, no orchestrator (Kubernetes, ECS,
Cloud Run) can safely scale or replace unhealthy replicas. Observability
is also required to feed the cloud-provider carbon dashboard (AR05).

## Decision

Every service MUST expose:

- `/health` (liveness) — 200 when the process is up.
- `/health/ready` (readiness) — 200 only when dependencies are reachable.
- `/metrics` (Prometheus format) — service-level SLIs.

Frameworks: Spring Actuator, FastAPI `starlette.responses`, ASP.NET Core
`AddHealthChecks()` + `prometheus-net`.

## Consequences

- Enables auto-scaling (AR04) and safe rolling deploys.
- **Verified in CI** by probing well-known health paths.

