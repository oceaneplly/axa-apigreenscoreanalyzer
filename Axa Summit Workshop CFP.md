Title: Green Architecture: less fat, more impact, more efficiency!
(Java · Python · C# — same tools, same score, same CI gate)

Abstract:

Your APIs gained weight? They eat more CPU, RAM and bandwidth than needed?
Time to open the toolbox and give them a **Green relooking** — with numbers,
not vibes.

In this hands-on workshop we apply the **API Green Score** framework
(**100 pts of code rules + 23 pts of architecture rules = 123 pts total**)
on a real API and prove the gains **live**, using 100 % open-source tooling
that runs on **Java, Python and C# without a single line of glue code**.

The observation is simple: modern APIs are often resource-hungry.
The problem is not principles — everyone agrees APIs should be sober.
The problem is the absence of **measurable, automatable, and CI-enforced
rules**. So we bring them.

Live coding, in **3 acts**:

**🎬 Act 1 — Measure (baseline)**
- Auto-discover the OpenAPI spec of any running API.
- Hit every endpoint and compute per-endpoint payload / latency / cache
  score, energy consumption (Wh) and carbon emissions (gCO₂e).
- Aggregate into an interactive dashboard with per-rule drill-down.

**🛠️ Act 2 — Fix the code (Creedengo static rules)**
Same rule catalogue, three languages, one command

Then apply the **actionable API rules**: GZIP/Brotli compression (DE01),
`fields` filtering (DE08), mandatory pagination (DE11), ETag/304 caching
(DE02/DE03), `/changes` delta sync (DE06), Range/206 partial content,
CBOR binary payload (BIN01), `/health` + `/metrics` (LO01), rate limiting
with 429 + `Retry-After` (US07).

**🏛️ Act 3 — Fix the architecture (23 pts often forgotten!)**
- **AR01** Event-Driven: migrate polling to SSE / AsyncAPI / webhooks —
  auto-detected by the **EDA Migration Advisor**.
- **AR02** Runtime close to consumers: CDN edge headers, TLS handshake
  latency, multi-region servers, optional GeoIP anycast check.
- **AR03** One API per business need: cross-target Jaccard duplicate
  detection + intra-spec `v1/v2` cohabitation warning.
- **AR04** Scalable infra: HPA, KEDA, Terraform / Bicep autoscale,
  serverless dependency scan.
- **AR05** Cloud footprint dashboard: AWS / Azure / GCP native trackers.

**📜 The ADR gate** (new!)
Every architecture decision becomes a versioned **Architecture Decision
Record** (`docs/adr/*.md`) that the analyzer **auto-verifies on each PR**.
A broken ADR fails the build — no drift, no regression, no "we forgot".

**🚦 CI enforcement (before/after live)**
- GitHub Actions workflow (provided out-of-the-box).
- SonarQube quality gate wired to Creedengo rules.
- Spectral for OpenAPI linting.
- SVG badge auto-updated in the README.
- Threshold gate: fail the pipeline below your target Green Score.

**Result?** A lighter, faster API, with a reduced carbon footprint — and a
**CI gate** that prevents any future regression on push and PR.
We show the gains **live** (before/after): reduced network traffic,
stabilized latency, optimized cache, plus the architecture radar chart
going green.

**🎁 What you leave with:**
- A GitHub repo with the analyzer, the interactive dashboard, and
  **3 sample apps** (Java Spring Boot, Python FastAPI, C# ASP.NET Core).
- **10 ready-to-use ADRs** covering pagination, cache, compression,
  observability, events-over-polling, multi-region, autoscaling…
- A ready-to-copy `.github/workflows/green-score.yml`.
- A green SVG badge for your README.
- The full workshop roadmap (`docs/WORKSHOP-ROADMAP.md`) so you can
  re-play the workshop with your own team.

Dashboard demo: https://thiernodialloafa.github.io/green-api-workshop-final/
