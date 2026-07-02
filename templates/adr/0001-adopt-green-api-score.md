---
adr: 0001
title: Adopt the API Green Score framework
status: accepted
date: 2026-07-02
green_rules: []
verifies: []
---

# 0001 — Adopt the API Green Score framework

## Context

Modern REST APIs consume network, CPU and storage without any systematic
measurement of their environmental footprint. The team needs a shared,
measurable and CI-enforceable baseline.

## Decision

We adopt the **API Green Score** framework (100 pts code + 23 pts
architecture) and the **Creedengo** static analyzer as the reference for
every backend service the team ships.

## Consequences

- Every service must publish a Green Score report on every PR.
- The score is displayed as a badge in the service README.
- Regressions below the configured `minScore` fail the build.
- Architecture decisions are tracked as ADRs verified automatically.

