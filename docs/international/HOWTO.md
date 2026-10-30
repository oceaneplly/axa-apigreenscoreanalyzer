# 🌱 HOW-TO — Using the AXA API Green Score Analyzer from A to Z

This guide is for **any new user** (beginners included) who wants to
run the analyzer:

- **locally (CLI)** — on their machine,
- **in GitHub Actions**,
- **in Azure DevOps Pipeline**,
- **in GitLab CI**,
- or via the **interactive UI** / the **standalone binary** / the **Docker container**.

> 💡 **In one sentence**: the main entry point is
> [`scripts/start.sh`](../../scripts/start.sh). It orchestrates EVERYTHING
> (app build, health-check, Green Score measurement, Creedengo eco-design
> analysis, SVG badge, HTML dashboard, ADR gate). All other scripts are
> building blocks called by `start.sh` — but you can also run them on their own.

---

## 📑 Table of contents

1. [Prerequisites](#1-prerequisites)
2. [Quick start (30 seconds)](#2-quick-start-30-seconds)
3. [`start.sh` — the main entry point](#3-startsh--the-main-entry-point)
   - [All flags](#31-all-startsh-flags)
   - [Environment variables](#32-environment-variables)
   - [Common CLI recipes](#33-common-cli-recipes)
4. [Other entry points](#4-other-entry-points)
   - [Green Score analysis alone](#41-green-score-alone)
   - [Creedengo analysis alone](#42-creedengo-alone)
   - [Offline OpenAPI lint](#43-offline-openapi-lint)
   - [Interactive UI (local server)](#44-interactive-ui)
   - [Standalone binaries](#45-standalone-binaries)
   - [Docker container](#46-docker-container)
   - [Dashboard & badge](#47-dashboard--badge)
   - [Sending to SobriIT](#48-sending-to-sobriit)
   - [Installing into another repo](#49-installing-into-another-repo)
5. [CI/CD integration](#5-cicd-integration)
   - [GitHub Actions](#51-github-actions)
   - [Azure DevOps](#52-azure-devops)
   - [GitLab CI](#53-gitlab-ci)
   - [Pre-commit hook](#54-pre-commit-hook-local)
6. [Understanding the results](#6-understanding-the-results)
7. [Troubleshooting (FAQ)](#7-troubleshooting-faq)

---

## 1. Prerequisites

| Need | Detail |
|--------|--------|
| **Bash** | Required. On Windows, use **Git Bash** or **WSL** (not PowerShell directly for `start.sh`). |
| **Python** | 3.10+ with `pip`. Install deps: `pip install -r scripts/requirements.txt`. |
| **Java** (if Java stack) | JDK 17+ and Maven 3.8+ (or the project's `./mvnw` wrapper). |
| **.NET** (if C# stack) | .NET SDK 8.0+ (`dotnet --version` ≥ 8). |
| **Container runtime** | Docker **or** Podman — required only for Creedengo (SonarQube). |
| **curl, git** | Used for health-checks and repo cloning. |

> ℹ️ `start.sh` **auto-installs** Maven / .NET SDK locally (without sudo) if
> missing, and automatically detects Docker or Podman.

---

## 2. Quick start (30 seconds)

You already have an API running on `http://localhost:8080`:

```bash
# 1. Install Python dependencies (once)
pip install -r scripts/requirements.txt

# 2. Analyze the API (Green Score only)
bash scripts/start.sh --target http://localhost:8080
```

Results produced:
- `reports/latest-report.json` — detailed report,
- `badges/green-score.svg` — score badge,
- `dashboard/index.html` — interactive dashboard, automatically opened in the
  browser by `start.sh` when running locally.

---

## 3. `start.sh` — the main entry point

`start.sh` chains, in order:

1. **(optional) Git clone** (`--git-repo`) or use of a local folder (`--source-dir`).
2. **(optional) Build & run** of the API locally (`--build-and-run`).
3. **Health-check** of the targets (`/actuator/health`, `/health`, `/`…).
4. **OpenAPI discovery + measurement** → **Green Score** (100 pts).
5. **Architecture rules** AR01–AR05 (+23 pts) and **ADR gate**.
6. **(optional) Creedengo** — eco-design code analysis (`--creedengo`).
7. **(optional) SobriIT submission** (`--send-to-sobriit`).
8. **SVG badge + HTML dashboard**.

### 3.1 All `start.sh` flags

| Flag | Effect |
|------|-------|
| `--target <url>` | URL of an API to analyze. **Repeatable**. |
| `--targets <csv>` | Comma-separated list of URLs (`http://a:8080,http://b:8082`). |
| `--swagger <url\|file>` | Explicit OpenAPI spec (otherwise auto-discovery). Repeatable. |
| `--swaggers <csv>` | Comma-separated list of specs. |
| `--bearer <token>` | ****** for protected endpoints. |
| `--appname <name>` | Application name in reports (default: folder name). |
| `--stack <auto\|java\|dotnet>` | Forces the stack; `auto` detects from `--source-dir`. |
| `--source-dir <path>` | Local source code folder (build, AR01/AR04, Creedengo). |
| `--build-and-run` | Compiles **and** starts the API before analysis. Requires `--source-dir`. |
| `--creedengo` | Enables the Creedengo eco-design analysis (requires Docker/Podman). |
| `--git-repo <url>` | Clones a remote repo (single source for build + Creedengo). Implies `--creedengo`. |
| `--git-branch <b>` | Branch/tag to check out. |
| `--git-subdir <p>` | Analyze a subfolder of the cloned repo. |
| `--git-keep` | Keep the clone after analysis (otherwise deleted). |
| `--root <path>` | Explicit project folder for Creedengo. |
| `--adr-dir <path>` | ADR folder to check (default: `docs/adr`). |
| `--fail-on-adr-violation` | Fails the build if an ADR with `status: accepted` fails. |
| `--consumer-region <ISO2>` | Consumer region (AR02, e.g. `FR`, `US`). |
| `--enable-geoip` | Enables the GeoIP check (ipinfo.io) for AR02 anycast/ASN. |
| `--cloud-footprint-confirmed` | Attests use of the cloud carbon dashboard (validates AR05). |
| `--send-to-sobriit` | Sends results to the SobriIT platform. |
| `--app-code <code>` | SobriIT application code. |
| `--debug` | Verbose mode. |

> 🔁 Flags also accept the `--flag=value` form for `--stack`,
> `--source-dir`, `--consumer-region`, `--adr-dir`.

### 3.2 Environment variables

Alternatives to flags (handy in CI):

| Variable | Equivalent flag |
|----------|-----------------|
| `BEARER_TOKEN` | `--bearer` |
| `APPNAME` | `--appname` |
| `CONSUMER_REGION` | `--consumer-region` |
| `ENABLE_GEOIP=true` | `--enable-geoip` |
| `CLOUD_FOOTPRINT_CONFIRMED=true` | `--cloud-footprint-confirmed` |
| `ADR_DIR` | `--adr-dir` |
| `FAIL_ON_ADR_VIOLATION=true` | `--fail-on-adr-violation` |
| `SOBRIIT_APP_CODE` | `--app-code` |
| `SOBRIIT_BASE_URL`, `SOBRIIT_API_KEY`, `SOBRIIT_APP_DSI`, `SOBRIIT_APP_TRIBE`, `SOBRIIT_APP_TRIBE_ID` | SobriIT config |
| `JAVA_MODULE` | Forces the Maven submodule to run (multi-module). |
| `LOMBOK_VERSION` | Forces the patched Lombok version for the Java build. |
| `SONAR_PORT` | Creedengo SonarQube port (default: 9100). |

### 3.3 Common CLI recipes

```bash
# ── API already started, Green Score only ─────────────────────────────
bash scripts/start.sh --target http://localhost:8080

# ── Several APIs in one pass ─────────────────────────────────────
bash scripts/start.sh --targets http://localhost:8080,http://localhost:8082

# ── Protected endpoints (bearer token) ───────────────────────────────
bash scripts/start.sh --target http://localhost:8080 --bearer "******"
# or:
BEARER_TOKEN=****** bash scripts/start.sh --target http://localhost:8080

# ── Java: automatic build + run + Creedengo ──────────────────────
bash scripts/start.sh --stack java --build-and-run \
                      --source-dir ./my-spring-app --creedengo

# ── .NET: automatic build + run + Creedengo ──────────────────────
bash scripts/start.sh --stack dotnet --build-and-run \
                      --source-dir ./MyAspNetApi --creedengo \
                      --target http://localhost:5050

# ── Auto-detect the stack from the source folder ────────────────
bash scripts/start.sh --stack auto --source-dir . --build-and-run --creedengo

# ── Analyze a remote repo without a local copy ──────────────────
bash scripts/start.sh --git-repo https://github.com/org/repo.git \
                      --git-branch main --creedengo

# ── ADR gate (fails if an "accepted" ADR is not respected) ─
bash scripts/start.sh --source-dir . --adr-dir docs/adr --fail-on-adr-violation

# ── Full architecture scoring (AR02 + AR05) ──────────────────────
bash scripts/start.sh --target http://localhost:8080 \
                      --consumer-region FR --enable-geoip \
                      --cloud-footprint-confirmed

# ── Enable everything + SobriIT submission ────────────────────────────────
bash scripts/start.sh --stack auto --source-dir . --build-and-run \
                      --creedengo --adr-dir docs/adr --fail-on-adr-violation \
                      --send-to-sobriit --app-code MYAPP
```

> ⚠️ **Paths with spaces**: quote them →
> `--source-dir "/path/with spaces/project"`.

---

## 4. Other entry points

All these scripts are called by `start.sh`, but remain usable on their own.

### 4.1 Green Score alone

Discovery + measurement wrapper (no Creedengo, no build):

```bash
# Via environment variables
TARGET_URL=http://localhost:8080 \
  bash scripts/green-score-analyzer_withdiscovery.sh --debug
```

Or directly the Python engine (the most flexible):

```bash
python3 scripts/green-api-auto-discover.py \
  --target http://localhost:8080 \
  --swagger http://localhost:8080/v3/api-docs \
  --appname my-api \
  --repeat 3 \
  --methods get,post \
  --output-dir reports/
```

Useful flags of `green-api-auto-discover.py`:

| Flag | Effect |
|------|-------|
| `--target <url>` | API base URL (repeatable or CSV). |
| `--swagger <url\|file>` | OpenAPI spec (repeatable or CSV). |
| `--bearer <token>` | Authentication. |
| `--param key=value` | Injected path/query parameter (repeatable). |
| `--repeat <n>` | Number of measurements per endpoint (default: 3). |
| `--methods <csv>` | HTTP methods (default: get,post,put,patch,delete). |
| `--dry-run` | Lists endpoints without calling them. |
| `--source-dir <path>` | Source code (AR01/AR04). |
| `--adr-dir <path>` | ADR folder (auto-detected: `./docs/adr` or `./adr`). |
| `--fail-on-adr-violation` | Exit ≠ 0 if an ADR fails. |
| `--consumer-region <code>` / `--enable-geoip` | AR02. |
| `--cloud-footprint-confirmed` | AR05. |
| `--output-dir <dir>` | Output folder (default: `reports/`). |

### 4.2 Creedengo alone

Static eco-design analysis of the **source code** (Java / Python / C#) via
SonarQube + Creedengo plugin (requires Docker/Podman):

```bash
# Local folder
bash scripts/creedengo-analyzer.sh --root ./my-app --lang java

# Remote repo
bash scripts/creedengo-analyzer.sh \
  --git-repo https://github.com/org/repo.git --git-branch main --lang csharp
```

| Flag | Effect |
|------|-------|
| `--root <path>` | Project folder (default: current folder). |
| `--lang <java\|python\|csharp\|dotnet>` | Forces the language. |
| `--git-repo/--git-branch/--git-subdir/--git-keep` | Git cloning. |
| `--skip-build` | Don't rebuild. |
| `--no-cleanup` | Leaves SonarQube running (accessible on `http://localhost:9100`). |
| `--force-cleanup` | Destroys SonarQube containers/volumes/images. |
| `--skip-dashboard` | Don't regenerate the dashboard. |
| `--debug` | Verbose. |

Output: `reports/creedengo-report.json`.

### 4.3 Offline OpenAPI lint

Checks the **static** Green API rules on a spec, **without calling the API**
(ideal for fast CI / pre-commit):

```bash
python3 scripts/green-api-lint.py openapi.yaml --format text
python3 scripts/green-api-lint.py openapi.yaml --format json  --fail-on-warn
python3 scripts/green-api-lint.py openapi.yaml --format sarif > lint.sarif
```

Exit codes: `0` = OK · `1` = findings (+ `--fail-on-warn`) · `2` = invalid file.

### 4.4 Interactive UI

Local web dashboard to run analyses from a browser:

```bash
bash scripts/start-interactive.sh              # http://127.0.0.1:8765
bash scripts/start-interactive.sh --port 9000 --no-open
```

Internally it runs `greenapianalyzer-server.py` which exposes:

- `GET /` → the UI (`dashboard/interactive.html`),
- `POST /api/discover` → discovery of target OpenAPI specs,
- `POST /api/analyze` → runs the analysis and returns `latest-report.json`.

**"Local Green Score / Creedengo Source analyse"** tab: stack selector,
source folder, build & run checkbox, live log console.

### 4.5 Standalone binaries

To distribute the tool without dependencies:

```bash
# Full binary (analyze + lint + serve)
bash scripts/build-binary.sh --output dist/greenanalyzer

# Usage
dist/greenanalyzer analyze --target http://localhost:8080
dist/greenanalyzer lint openapi.yaml
dist/greenanalyzer serve --port 8765

# Light binary (OpenAPI lint only, ~20 KB)
bash scripts/build-lint-binary.sh --output dist/green-api-lint
dist/green-api-lint openapi.yaml --format json
```

### 4.6 Docker container

The image embeds Python, Spectral, curl, jq and all the scripts.
The `ENTRYPOINT` is the `green-api-auto-discover.py` engine:

```bash
# Build
docker build -t greenanalyzer .

# Analyze an API (the args are passed to the analyzer)
docker run --rm greenanalyzer --target http://host.docker.internal:8080

# Lint a spec mounted as a volume
docker run --rm -v "$PWD:/work" greenanalyzer \
  lint /work/openapi.yaml --format json
```

### 4.7 Dashboard & badge

Manually regenerate from an existing report:

```bash
# HTML + Markdown dashboard
bash scripts/generate-dashboard.sh reports/latest-report.json \
     dashboard/index.save.html dashboard/index.html reports/creedengo-report.json

# SVG badge
bash scripts/generate-badge.sh reports/latest-report.json badges/green-score.svg
```

### 4.8 Sending to SobriIT

Directly (without going through `start.sh`):

```bash
python3 scripts/sobriit_sender.py \
  --appname my-api \
  --green-report reports/latest-report.json \
  --creedengo-report reports/creedengo-report.json \
  --app-code MYAPP
```

Config via env: `SOBRIIT_BASE_URL`, `SOBRIIT_API_KEY`, `SOBRIIT_APP_CODE`,
`SOBRIIT_APP_DSI`, `SOBRIIT_APP_TRIBE`, `SOBRIIT_APP_TRIBE_ID`.

### 4.9 Installing into another repo

`installer.sh` clones a target repo, creates a branch and copies all the tooling
into it (scripts, dashboard, badges, `.creedengo/`, GitHub workflow, `.spectral.yml`,
`green-score-threshold.json`):

```bash
bash installer.sh https://github.com/org/my-api.git
```

---

## 5. CI/CD integration

The principle is **identical everywhere**: install the toolchains → (optional)
start SonarQube → run `start.sh` → gate on `green-score-threshold.json`
→ publish `reports/` and `badges/`.

The `green-score-threshold.json` file defines the minimum score:

```json
{ "minScore": 85, "note": "Below this, the CI fails." }
```

Suggested scale: **60** (POC/legacy) · **85** (production) · **100+** (critical).

### 5.1 GitHub Actions

Copy [`templates/ci/green-score.yml`](../../templates/ci/green-score.yml) into
your repo's `.github/workflows/`. It already does everything:

- Sets up **JDK 17 + Python 3.11 + .NET 8**,
- Starts an ephemeral SonarQube,
- Runs `start.sh --stack auto --source-dir . --build-and-run --creedengo --adr-dir docs/adr --fail-on-adr-violation`,
- Applies the `green-score-threshold.json` gate,
- Uploads `reports/` + `badges/`,
- Automatically commits the SVG badge to `main`.

Only required config: the **`API_BEARER_TOKEN`** secret (if your API is protected).

Key excerpt:

```yaml
- name: Build & run + Green Score + Creedengo + ADR gate
  run: |
    bash scripts/start.sh --stack auto --source-dir . \
         --build-and-run --creedengo \
         --adr-dir docs/adr --fail-on-adr-violation
  env:
    BEARER_TOKEN: ${{ secrets.API_BEARER_TOKEN }}
```

### 5.2 Azure DevOps

```yaml
trigger: [main]

pool:
  vmImage: ubuntu-latest

steps:
  - task: UseJavaVersion@1
    inputs: { versionSpec: '17' }

  - task: UsePythonVersion@0
    inputs: { versionSpec: '3.11' }

  - task: UseDotNet@2
    inputs: { version: '8.0.x' }

  - script: |
      docker run -d --name sonarqube -p 9000:9000 \
        -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true sonarqube:community
      for i in {1..36}; do
        curl -sf http://localhost:9000/api/system/status | grep -q '"UP"' && break
        sleep 5
      done
    displayName: Start SonarQube

  - script: |
      python3 -m pip install --upgrade pip
      pip install -r scripts/requirements.txt
    displayName: Install analyzer deps

  - script: |
      bash scripts/start.sh --stack auto --source-dir . \
                            --build-and-run --creedengo \
                            --adr-dir docs/adr --fail-on-adr-violation
    displayName: Green Score + ADR gate
    env:
      BEARER_TOKEN: $(API_BEARER_TOKEN)

  - task: PublishBuildArtifacts@1
    condition: always()
    inputs:
      pathToPublish: reports
      artifactName: green-score-reports
```

> 🔐 Define `API_BEARER_TOKEN` in **Pipelines → Library** (secret variable).

### 5.3 GitLab CI

```yaml
green-score:
  image: ubuntu:22.04
  services:
    - name: sonarqube:community
      alias: sonarqube
      variables:
        SONAR_ES_BOOTSTRAP_CHECKS_DISABLE: "true"
  variables:
    DOCKER_HOST: tcp://docker:2375
  before_script:
    - apt-get update && apt-get install -y curl git openjdk-17-jdk python3 python3-pip
    - curl -fsSL https://dot.net/v1/dotnet-install.sh | bash -s -- --channel 8.0
    - pip3 install -r scripts/requirements.txt
  script:
    - bash scripts/start.sh --stack auto --source-dir .
                            --build-and-run --creedengo
                            --adr-dir docs/adr --fail-on-adr-violation
  artifacts:
    when: always
    paths:
      - reports/
      - badges/
    expire_in: 30 days
```

### 5.4 Pre-commit hook (local)

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
set -e
# Fast: offline OpenAPI lint (no need for a running app)
python3 scripts/green-api-lint.py openapi.yaml --fail-on-warn

# OR full: ADR gate + Green Score
bash scripts/start.sh --stack auto --source-dir . \
                      --adr-dir docs/adr --fail-on-adr-violation
```

---

## 6. Understanding the results

| File | Content |
|---------|---------|
| `reports/latest-report.json` | Full Green Score report (100 pts code + 23 architecture). |
| `reports/creedengo-report.json` | Eco-design findings (GCI rules). |
| `reports/discovered-openapi.json` | Merged OpenAPI specs of the targets. |
| `badges/green-score.svg` | Score badge (to embed in a README). |
| `dashboard/index.html` | Interactive dashboard (open in a browser). |
| `dashboard/index.md` | Markdown version of the dashboard. |

The **total score is out of 123 pts**: 100 pts of code rules (DE11 pagination,
DE08 filtering, DE01 gzip, DE02/03 ETag cache, DE06 delta, 206 range, binary
format, LO01 observability, US07 rate-limit) + 23 architecture pts
(AR01 event-driven, AR02 runtime proximity, AR03 single API, AR04 scalability,
AR05 cloud footprint).

---

## 7. Troubleshooting (FAQ)

| Symptom | Solution |
|----------|----------|
| **`start.sh` won't run on Windows** | Use **Git Bash** or **WSL** (not PowerShell/cmd). |
| **"Targets not ready" timeout** | The API did not respond on `/health`/`/actuator/health`/`/`. Check the URL and port; increase the startup time. |
| **`--build-and-run`: stack not detected** | Specify `--stack java` or `--stack dotnet`. Clues searched: `pom.xml`, `build.gradle`, `*.csproj`, `*.sln`. |
| **Java multi-module: wrong module started** | Force with `JAVA_MODULE=<module-name>`. |
| **Lombok compilation errors** | `LOMBOK_VERSION=1.18.34 bash scripts/start.sh …` (auto-patch in a disposable checkout). |
| **Creedengo won't start** | Docker/Podman required. SonarQube runs on `http://localhost:9100` (configurable via `SONAR_PORT`). |
| **Protected endpoints → 401** | Provide `--bearer <token>` or `BEARER_TOKEN=…`. |
| **C#: HTTPS dev-cert prompt** | `ASPNETCORE_URLS=http://+:<port>` (HTTP) is forced to avoid the prompt. |
| **First `dotnet restore` very slow** | Empty NuGet cache — normal the 1st time (extended timeout). |
| **Java + .NET mono-repo** | Use explicit `--stack` to remove ambiguity. |

---

📚 See also:
[README](../../README.md) ·
[CI-INTEGRATION](CI-INTEGRATION.md) ·
[ADR templates](../templates/adr/) ·
[Sample apps](../samples/).
