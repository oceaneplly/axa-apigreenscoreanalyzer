# 📋 CFP promises → Analyzer capabilities coverage

> 1↔1 mapping of the `Axa Summit Workshop CFP.md` CFP promises to the
> capabilities implemented in the analyzer. This matrix can be checked
> automatically in CI (`scripts/check-promises-coverage.py`).
>
> **Legend**: ✅ implemented · 🟡 partial · ❌ missing

Last updated: 2026-07-02

---

## 1. Green Score — eco-design rules (100 pts)

| CFP promise | Rule | ID | Weight | Status | Analyzer component |
|---|---|---|---:|---|---|
| GZIP/Brotli compression | Compression | DE01 | 15 | ✅ | `green-api-auto-discover.py` (probe `Accept-Encoding`) |
| Partial fields | Field filtering | DE08 | 15 | ✅ | `?fields=` probe |
| Mandatory pagination | Pagination | DE11 | 15 | ✅ | Detects `page/size/limit/offset` |
| ETag / 304 cache | Cache ETag | DE02/03 | 15 | ✅ | `If-None-Match` probe |
| `/changes` delta sync | Delta | DE06 | 10 | ✅ | Detects `?since=<ts>` |
| Range / 206 Partial | Range | 206 | 10 | ✅ | `Range: bytes=` probe |
| Binary payload | Binary | BIN01 | 10 | 🟡 | `Accept: application/cbor|x-protobuf|msgpack` probe (to be extended) |
| Observability | Health/Metrics | LO01 | 5 | ✅ | Probes `/health`, `/metrics`, `/actuator/health` |
| Rate limiting | 429 | US07 | 5 | ✅ | Detects `429` + `Retry-After` |

**Total code: 100 pts**

## 2. Architecture & Infrastructure (23 pts)

| Rule | ID | Weight | Status | Signals |
|---|---|---:|---|---|
| Event-Driven | AR01 | 6 | ✅ | OAS callbacks · 3.1 webhooks · AsyncAPI · SSE runtime · broker deps |
| Runtime proximity | AR02 | 7 | ✅ | CDN headers · TLS handshake · multi-region · GeoIP (opt.) |
| Single API | AR03 | 3 | ✅ | Jaccard signatures · tags · cosine · intra v1/v2 |
| Scalable infra | AR04 | 5 | ✅ | HPA · KEDA · Terraform · Bicep · Serverless · FaaS deps |
| Cloud footprint | AR05 | 2 | ✅ | Provider auto-detect · observability probe · attestation |

**Total architecture: 23 pts** → workshop total = **123 pts**.

## 3. Creedengo static rules (per stack)

| Stack | Status | Wrapper | Key rules (excerpt) |
|---|---|---|---|
| Java (Maven/Gradle) | ✅ | SonarQube D1 plugin (`creedengo-java`) | GCI1, GCI3, GCI5, GCI69, GCI72, GCI74, GCI76, GCI77, GCI79, GCI82, GCI94 |
| C# / .NET 8+ | ✅ | D1 (`creedengo-csharp`) otherwise D2 stock SQ fallback | GCI69, GCI72, GCI75, GCI81, GCI83, GCI84, GCI85, GCI86, GCI87, GCI88, GCI91, GCI92, GCI93 |
| Python 3.10+ | ✅ | SonarQube D1 plugin (`creedengo-python`) | GCI72, GCI74, GCI89, GCI103, GCI105, GCI109, GCI110, GCI111, GCI112, GCI404 |
| JavaScript / TypeScript | 🟡 | plugin detected but not promoted in the CFP | — |
| F# / VB.NET | ❌ | not covered by Creedengo (explicit warning) | — |

## 4. Pipelines & CI

| Provider | Status | File |
|---|---|---|
| GitHub Actions | ✅ | `templates/ci/green-score.yml` |
| GitLab CI | ✅ | `docs/CI-INTEGRATION.md` (snippet) |
| Azure DevOps | ✅ | `docs/CI-INTEGRATION.md` (snippet) |
| Threshold gate | ✅ | `green-score-threshold.json` (`minScore`) |
| Badge SVG | ✅ | `badges/green-score.svg` + `scripts/generate-badge.sh` |

## 5. ADR framework (new)

| Capability | Status | File |
|---|---|---|
| MADR format + YAML front-matter | ✅ | `templates/adr/*.md` (10 ADRs) |
| Automatic verification | ✅ | `scripts/adr_rules.py` |
| Dashboard integration | ✅ | "ADR compliance" section (radar + table) |
| CI gate (`--fail-on-adr-violation`) | ✅ | CLI flag + exit code |

## 6. Workshop deliverables

| Deliverable | Status | Path |
|---|---|---|
| Sample Java Spring Boot app | ✅ | `samples/java-spring/` |
| Sample Python FastAPI app | ✅ | `samples/python-fastapi/` |
| Sample C# ASP.NET Core app | ✅ | `samples/csharp-aspnet/` |
| 10 starter ADRs | ✅ | `templates/adr/` |
| GitHub Actions workflow | ✅ | `templates/ci/green-score.yml` |
| Facilitator roadmap | ✅ | `docs/WORKSHOP-ROADMAP.md` |
| Interactive dashboard | ✅ | `dashboard/index.html` |
| SVG badge | ✅ | `badges/green-score.svg` |

---

## 🔄 Regeneration

This matrix can be regenerated via:

```bash
python3 scripts/check-promises-coverage.py > docs/PROMISES-COVERAGE.md
```

The script fails (exit ≠ 0) if one of the components marked ✅ does not exist
in the tree → documentation anti-regression gate.
