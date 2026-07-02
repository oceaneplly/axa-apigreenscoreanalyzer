---
adr: 0009
title: Auto-scaling and serverless where applicable (AR04)
status: accepted
date: 2026-07-02
green_rules: [AR04]
verifies:
  - kind: iac_signal
    signal: hpa
    any_of: [hpa, keda, terraform-autoscale, bicep-autoscale, serverless-config, faas-deps]
---

# 0009 — Auto-scaling and serverless where applicable

## Context

Over-provisioning idle infrastructure is the largest single source of
wasted energy in cloud environments. Auto-scaling and FaaS eliminate the
"always-on" baseline for spiky or infrequent workloads.

## Decision

Every service MUST express at least one **auto-scaling signal** in its
IaC or build files, matching one of:

- Kubernetes HPA (`HorizontalPodAutoscaler`) or KEDA `ScaledObject`.
- Terraform / Bicep autoscale resource.
- Serverless framework / SAM / Azure Functions / GCF config.
- FaaS dependency in `pom.xml` / `.csproj` / `requirements.txt`.

## Consequences

- Idle capacity reduced to a strict minimum.
- **Verified in CI** via the `iac_signal` checker (Phase-2 scan of
  `--source-dir`).

