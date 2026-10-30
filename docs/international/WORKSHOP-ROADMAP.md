# 🗺️ Workshop Roadmap — Green Architecture

> Replayable by any facilitator. Two formats: **2 h (Summit)** and
> **3 h (standalone workshop)**. Stacks: **Java · Python · C#** (participant's
> choice, no glue code to write).

---

## 🎯 Learning objectives

By the end of the workshop, each participant is able to:

1. Measure the **Green Score** (code + architecture) of an existing API.
2. Apply 5 quick wins that raise the score by +30 to +40 points.
3. Document green architecture decisions via **ADRs** automatically
   verified in CI.
4. Wire everything into **your CI/CD** with an anti-regression gate.

---

## ✅ Participant prerequisites

- **Git** + editor (VS Code / IntelliJ / Rider).
- **Docker Desktop** or **Podman** (local SonarQube).
- One of the three stacks, participant's choice:
  - Java 17+ + Maven 3.8+
  - Python 3.10+
  - .NET SDK 8.0+
- ~10 GB free disk space (Docker images + NuGet/Maven cache).

Kit to clone **before** the workshop:

```bash
git clone https://github.com/<org>/axa-apigreenscoreanalyzer.git
cd axa-apigreenscoreanalyzer
bash installer.sh           # installs deps, warms up Docker
```

---

## ⏱️ Short format — 2 h (Summit "hands-on" slot)

| # | Duration | Block | Content | Deliverable / Checkpoint |
|---|-------|------|---------|-----------------------|
| 0 | 5 min | **Kickoff** | Green IT context · key figures (IT footprint ~4% global CO₂e) · workshop objectives | — |
| 1 | 15 min | **Setup** | Clone, `bash installer.sh`, choose stack (Java/Python/C#), start sample app (`samples/<stack>/`) | App UP on port 8080/8000/5050 |
| 2 | 20 min | **Act 1 — Measure** | `bash scripts/start.sh --target http://localhost:<port> --source-dir samples/<stack>` → baseline dashboard | Baseline score visible in `reports/latest-report.json` |
| 3 | 25 min | **Act 2 — Code quick-wins** | Apply 5 fixes: DE11 pagination · DE01 GZIP · DE08 `fields` · DE02/03 ETag · DE06 `/changes` | Overall score **+30 pts** minimum |
| 4 | 25 min | **Act 3 — Architecture** | AR01 SSE instead of polling · AR03 v1/v2 dedup · AR04 HPA/serverless example · AR05 provider dashboard | ≥ 3 AR* rules pass ✅ |
| 5 | 15 min | **ADR gate** | Add 3 ADRs (`docs/adr/`), deliberately break 1 ADR, fix it | `reports/adr-report.json` OK |
| 6 | 10 min | **CI wiring** | Copy `.github/workflows/green-score.yml`, push, watch the run + badge | Green workflow + updated SVG badge |
| 7 | 5 min | **Wrap-up** | Q&A · resources · Creedengo & API Green Score OSS roadmap | — |

---

## ⏱️ Long format — 3 h (standalone workshop)

Reuses the short format + 3 additional 30-min blocks:

| # | Duration | Block | Content | Deliverable |
|---|-------|------|---------|----------|
| 3-bis | 30 min | **BIN01 & binary payload** | Add an endpoint `Accept: application/cbor` (e.g. via `cbor2`, `Jackson-CBOR`, `MessagePack`) and measure payload reduction | −40% to −60% bytes |
| 4-bis | 30 min | **Advanced AR02** | `--consumer-region FR --enable-geoip` · reading TLS handshake · multi-region plan | AR02 = 7/7 |
| 6-bis | 30 min | **Per-stack coaching (breakouts)** | Java / Python / C# groups — facilitator visits each table | Personal score per participant |

---

## 🎬 Act details

### Act 1 — Measure

**Commands**

```bash
# Stack of choice — the script auto-detects
bash scripts/start.sh \
     --stack auto \
     --source-dir samples/java-spring \
     --build-and-run \
     --creedengo
```

**What the participant should see in the dashboard:**
- Overall score out of 123 pts.
- "Architecture 23" banner **at the same level** as "Code 100".
- AR01→AR05 radar chart.
- Endpoint-by-endpoint table with bytes / latency / cache / ETag.

### Act 2 — Code quick-wins (Creedengo + rules)

Recommended order (decreasing impact):

1. **DE11 pagination** — add `?page`/`?size` to collections. +15 pts.
2. **DE01 compression** — GZIP middleware (Spring/FastAPI/ASP.NET). +15 pts.
3. **DE08 fields** — `?fields=id,name` filter. +15 pts.
4. **DE02/03 ETag** — payload hash + 304 on `If-None-Match`. +15 pts.
5. **DE06 delta** — `/changes?since=<ts>` endpoint. +10 pts.

Then re-run:

```bash
bash scripts/start.sh --target http://localhost:<port> --source-dir samples/<stack>
```

### Act 3 — Architecture (the "gap" to close in most APIs)

- **AR01** — remove `/changes` polling and expose an `/events` SSE endpoint
  (`text/event-stream`). See ADR `0007`.
- **AR03** — spot `v1/v2` duplicates detected by the report, mark
  v1 as `deprecated`.
- **AR04** — add an HPA example (`k8s/hpa.yaml`) OR a `serverless.yml`.
  The Phase 2 scan (`--source-dir`) must detect it.
- **AR05** — enable `--cloud-footprint-confirmed` OR expose `/metrics`.

### Act 4 — ADR gate

1. Copy the 10 provided ADRs from `templates/adr/` to `docs/adr/`.
2. Run:
   ```bash
   bash scripts/start.sh --source-dir . --adr-dir docs/adr --fail-on-adr-violation
   ```
3. Deliberately modify an endpoint to break ADR `0002-pagination`
   (remove `?page`). The CI must **fail**.
4. Fix it → green CI.

### Act 5 — CI wiring

```bash
mkdir -p .github/workflows
cp templates/ci/green-score.yml .github/workflows/
git add . && git commit -m "chore: green-score CI gate"
git push
```

Then:
- GitHub **Actions** tab → the run must be green.
- `badges/green-score.svg` updated and displayed in the README.

---

## 👨‍🏫 Facilitator guide — Checkpoints & fallbacks

At the end of each Act, the facilitator checks:

| Checkpoint | File to check | Fallback if KO |
|---|---|---|
| Act 1 baseline | `reports/latest-report.json` exists and contains `total_score` | Verify the app is UP (`curl :port/health`) |
| Act 2 quick-wins | `total_score` increased by ≥ 30 pts | Redo DE11 step-by-step (the most visual) |
| Act 3 architecture | ≥ 3 AR* rules with `matched: true` | Use `--cloud-footprint-confirmed` + copy the provided `k8s/hpa.yaml` |
| Act 4 ADR | `reports/adr-report.json` with ≥ 1 fail then pass | Redo the `0002-pagination` example |
| Act 5 CI | GitHub Actions run ✅ | Local fallback: `act` (nektos/act) |

---

## 📚 Resources provided (in the repo)

- `templates/adr/` — 10 starter ADRs.
- `templates/ci/green-score.yml` — GitHub Actions workflow.
- `samples/java-spring/` · `samples/python-fastapi/` · `samples/csharp-aspnet/`
- `docs/PROMISES-COVERAGE.md` — promises ↔ rules matrix.
- `docs/CI-INTEGRATION.md` — GitLab CI + Azure DevOps snippets.

---

## 🔗 External links

- API Green Score framework: https://github.com/AXA-GROUP-OPERATIONS/api-green-score
- Creedengo (formerly ecoCode): https://github.com/green-code-initiative
- Spectral: https://stoplight.io/open-source/spectral
- SonarQube: https://www.sonarsource.com/products/sonarqube/
