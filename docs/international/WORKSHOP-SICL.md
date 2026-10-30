# API Green Score Analyzer Workshop — SICL dev day

> Format: **1h30**, hands-on, in **pairs or trios**.
> Each team works on **an API running locally** on their machine.

---

## Workshop objective

By the end of the workshop, each team should have a dashboard with the API Green Score and Creedengo results for their project.

---

## Organization

| Item | Detail |
|---------|--------|
| Teams | 2 to 3 people. |
| Application | A SICL Java API. Failing that: a sample from [`samples/`](../samples/). |

### Agenda

| Block | Deliverable |
|------|----------|
| Step 1 — Start your API locally | API responds on `localhost`, Swagger accessible |
| Step 2 — Install the analyzer | Analyzer installed and first test run |
| Step 3 — Green API baseline analysis | Dashboard, initial report and score noted |
| Step 4 — Creedengo analysis | Creedengo score and most-violated rules noted |
| Step 5 — Debrief | Feedback on the workshop |
| Part 2 (bonus) — CI pipeline | Pipeline run on the PR |

---

## Prerequisites (to check before the workshop)

| Tool | Check | Note |
|-------|--------------|----------|
| JDK 17+ | `java -version` | |
| Python 3.10+ | `python --version` | |
| Bash | `bash --version` | On Windows: **Git Bash** or **WSL** (not PowerShell). |
| Git, curl | `git --version` / `curl --version` | |
| Podman | `podman --version` | **Only** for Creedengo (SonarQube). |

Clone the repo, switch branch (feat/atelier-journee-dev) and install the Python dependencies:

```bash
git clone https://axafrance@dev.azure.com/axafrance/GreenIT/_git/axa-apigreenscoreanalyzer
pip install -r scripts/requirements.txt
```
---

## Step 1 — Start your Java API locally

### 1.1 Choose the application

Choose a Java API that runs correctly on your machine (it should be fine normally🤓👆🏻)


### 1.2 Verify the API responds

Adjust the port if needed (default `8080`).

```bash
http://localhost:8080/actuator/health
http://localhost:8080/v3/api-docs or http://localhost:8080/swagger
```

### 1.3 Step checklist

- [ ] The application starts without error.
- [ ] A URL responds with `200` (e.g.: http://localhost:8080, http://localhost:8080/actuator/health).
- [ ] The OpenAPI contract is accessible (`/v3/api-docs` or `/swagger`) with `200`.
- [ ] If the API is protected: a test ******** is available (**never** commit it).


### Quick troubleshooting

| Symptom                         | Lead                                                                                                                                                                                                                                                       |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Port 8080 busy                 | Change `server.port` or stop the other process.                                                                                                                                                                                                         |
| 401/403 on Swagger              | Open the Swagger path in the security config under the local profile, or provide `--bearer`.                                                                                                                                                                 |
| Option A: `/swagger` missing     | In the `application.yml` or `application-local.yml` file, add the `/swagger` path to the `security.permit-all` section. Example: [Data Director file](https://dev.azure.com/axafrance/MDM/_git/client-data-director-bff?path=/clientdatadirector/src/main/resources/application.yml)                                                                                        |
| Option B: `/v3/api-docs` missing | Add the `springdoc-openapi-starter-webmvc-ui` dependency. Example: [Data Director commit](https://dev.azure.com/axafrance/MDM/_git/client-data-director-bff/commit/519a90d4a44e6a0a4d958d81eb22b5f0be814932?refName=refs%2Fheads%2Ffeat%2Fadd_pr_green) |
| Database required          | Use a `local` profile with an in-memory H2 database.                                                                                                                                                                                                     |

---

## Step 2 — Install the analyzer

From the root of the analyzer repo:
```bash
bash scripts/start.sh --target http://localhost:8080
```

- [ ] The script detects the API and finishes without error.
- [ ] `reports/latest-report.json` is created.
- [ ] `dashboard/index.html` opens.
- ⚠️️️ Change the port if needed (`--target http://localhost:<port>`).

Documentation on script.sh and its various parameters: [HOWTO.md file / Part 3](HOWTO.md).

---

## Step 3 — Green API baseline analysis

### 3.1 Run the analysis

**Option 1: the API is already running (strongly recommended)**

```bash
bash scripts/start.sh --target http://localhost:8080 --swagger http://localhost:8080/swagger --source-dir ./path/to/my-app --appname project-name
```

**Option 2: let the analyzer compile and start the API (after several hours of despair, I don't recommend it 🥲)**

```bash
bash scripts/start.sh --stack java --build-and-run --source-dir ./path/to/my-app --appname project-name
```
⚠️ Careful, you need to add the environment variables (especially SECRET) if the API needs them to start

**Option 3: API secured with a bearer token**

```bash
BEARER_TOKEN="<test-token>" bash scripts/start.sh --target http://localhost:8080
```

> Paths with spaces must be quoted.
> `--debug` enables diagnostic traces.

### 3.2 Read the dashboard

Open `dashboard/index.html` and note:

| Information | Score |
|-------------|--------------------|
| API Green Score (/100) | |
| Grade (A+ … E) | |
| Architecture score (/23) | |
| Failing rules (list) | |
| Most expensive endpoint (size / time) | |

### 3.3 Rules reminder

| Theme | Rules |
|-------|--------|
| Performance | Pagination (DE11), `fields` filtering (DE08), gzip compression (DE01) |
| Cache | ETag / 304 (DE02/DE03), `/changes` delta (DE06) |
| Scalability | Range / 206, Binary format (BIN01) |
| Observability / Protection | Health / Metrics (LO01), Rate limiting (US07) |
| Architecture | Event-driven (AR01), Runtime proximity (AR02), Single API (AR03), Infra scalability (AR04), Cloud footprint (AR05) |

**Team discussion**: which rules are failing, and which ones are the easiest to fix?

---

## Step 4 — Creedengo analysis

Creedengo analyzes the **source code** (eco-design anti-patterns) via SonarQube.
It requires Podman or Docker.

```bash
bash scripts/start.sh --stack java --source-dir ./path/to/my-app --target http://localhost:8080 --creedengo
```

Or standalone:

```bash
bash scripts/creedengo-analyzer.sh
```

Note in the dashboard:

| Information | Score |
|-------------|--------------------|
| Creedengo score (/100) | |
| Grade | |
| Most violated rules (GCI…) | |

Common Java rules: `GCI1` / `GCI72` (queries in loops), `GCI74` (`SELECT *`), `GCI77` (`Pattern.compile`), `GCI79` (try-with-resources), `GCI82` (`final` variables), `GCI94` (`orElseGet`).

> The API Green Score (running API) and the Creedengo score (source code) are **distinct**.

---

## Step 5 — Debrief

Each team completes and shares:

| Indicator | Score |
|------------|-------|
| API Green Score | |
| Grade | |
| Creedengo Score | |
| Rules fixed | |
| Difficulty encountered | |
| Recommendations | |

The previous report serves as a baseline: the dashboard shows the progress.

If you still have time, feel free to fix one or two rules in your code and compare before/after

---

## Part 2 — For the quickest: CI pipeline (bonus)

Integrate the analyzer into the project's pipeline (Azure DevOps or GitHub Actions). Templates: [`templates/ci`](../../templates/ci) and [CI-INTEGRATION.md](CI-INTEGRATION.md).

The pipeline (`pr-green-api-axa.yml`):

- triggers on **PR** and **weekly** (Sunday);
- installs JDK 17+, Maven and Python;
- clones the analyzer;
- runs `scripts/start.sh` with the parameters;
- analyzes Creedengo, Green Score and OpenAPI.

### Recommendations

| Topic | To check |
|-------|-----------|
| Variables | `TARGETS`, `SWAGGER_URL`, `STACK`, `BUILD_AND_RUN` set. |
| Swagger accessible | From the CI agent: authentication and `200` response on `/swagger` or `/v3/api-docs`. |
| Modules | Correct Maven/Gradle module names; right subdirectory targeted (`JAVA_MODULE`). |
| Secrets | `API_TOKEN`, `CLIENT_SECRET`, etc. in the CI's **secret** variables, never in the YAML or logs. |

💡 Example on Data Director (with a few hiccups, it was [great](https://dev.azure.com/axafrance/MDM/_build?definitionId=33895)):

- [ ] Pipeline added on a separate branch
- [ ] First run successful.
- [ ] Report / dashboard published as an artifact.

---

## General troubleshooting

| Problem | Solution |
|----------|----------|
| `start.sh` won't run on Windows | Use Git Bash or WSL. |
| No endpoint discovered | Provide `--swagger <url>` explicitly; check `200` on the OpenAPI contract. |
| Very low score everywhere | The API may be returning errors (401/500): check HTTP codes in the report. |
| Creedengo fails | Check that Podman/Docker is running; SonarQube port `9100` free (`SONAR_PORT`). |
| Java build fails (Lombok…) | `LOMBOK_VERSION=<version>`; for multi-module, `JAVA_MODULE=<module>`. |
| More details | Re-run with `--debug`. |

---

## Resources

- [Project README](../../README.md) · [HOWTO](HOWTO.md) · [CI Integration](CI-INTEGRATION.md)
- `dashboard/`: generated results
- [**API GreenScore v1.2** grid (PDF)](https://cdn.digitevent.com/69243f238739dbd18f49846f/websiteBtnFileUrl/0c90ba15-f0d0-4b1a-9fb4-ebd8dfb1717c-71-48-cat-sustainable-api-greenscore-v1-2.pdf)
- [Sobri-IT](https://sobri-it.axa-fr.intraxa/)
- Workshop slides: see the **atelier-project-structure.html** file
