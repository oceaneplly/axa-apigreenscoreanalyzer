# API Green Score Analyzer Workshop — Summit

> Format: **1 hour**, with hands-on exercises, to be completed **individually or in pairs**.
> The workshop offers three tracks: exploring the dashboard, scoring an API without a running API, or analyzing an
> already accessible application.

---

## Workshop objective

Explore the API Green Score dashboard and, depending on the resources available
to you, generate a report from an OpenAPI specification or a running API.
**No Java, .NET, or Python application is needed** for Parts 1 and 2.

---

## Prerequisites

| Tool | Required | Check | Notes |
|-------|--------|--------------|----------|
| Web browser | ✅ | — | No development tools required. |
| Git Bash | ✅ | `bash --version` | **Required** to run the workshop scripts. Do not use PowerShell, Command Prompt, or WSL. |
| Python 3.10+ | ✅ | `python --version` or `python3 --version` | Required to run all scripts: [Windows installer](https://www.python.org/ftp/python/pymanager/python-manager-26.4.msix), [macOS installer](https://www.python.org/ftp/python/3.15.2/python-3.15.2-macos11.pkg) |
| Docker or Podman | ❌ | — | Optional: required only for Part 4 (Creedengo), which starts SonarQube in a container. |
| Java | ❌ | — | Optional: you can use an existing application. |
| .NET | ❌ | — | Optional: you can use an existing application. |

Docker or Podman is not needed for Parts 1 to 3. Part 4 is optional and analyzes
source code; the API does not need to be running.

Clone the repository and install the analyzer dependencies from **Git Bash**:

```bash
git clone https://github.com/thiernodialloAFA/axa-apigreenscoreanalyzer.git
cd axa-apigreenscoreanalyzer
python -m pip install -r scripts/requirements.txt
```

---

## Part 1 — Explore the existing dashboard

This part is open to everyone, including people who do not develop APIs and do
not have a Java, .NET, or Python application.

1. Open the analyzer repository folder in File Explorer.
2. Open [dashboard/index.html](../../dashboard/index.html) in your web browser (for example, by double-clicking the file or choosing **Open with** and then selecting your browser).
3. Explore the API Green Score dashboard and its different sections. The dashboard displays a complete report that you can generate in Parts 2 or 3.

No terminal, API, or programming language is needed for this part.

---

## Part 2 — Generate a score from a Swagger/OpenAPI specification only

This part requires **neither a running API nor an application in any particular
language**. It uses `swagger-only` mode: the analyzer reads a Swagger file (JSON
or YAML) and sends no requests to the API endpoints.

> **Git Bash is required** for this part. Run the commands below in Git Bash,
> from the root of the cloned repository—not in PowerShell, Command Prompt, or
> WSL. You can also install the `Start git-bash` extension in VS Code.

### 2.1 Choose a specification

Use the workshop's sample specification, create a new one, or import a
specification from one of your existing applications. It must comply with the
supported OpenAPI standards and be available in JSON or YAML format. The
application does not need to be running for this part.

Run the following command using the [sample specification](../../dashboard/sample-swagger.yaml) in the project:

```bash
bash scripts/start.sh --swagger dashboard/sample-swagger.yaml --appname workshop-swagger-only
```

If your specification is available at a URL, replace the example path with its
URL, for example:

```bash
bash scripts/start.sh --swagger "https://petstore3.swagger.io/api/v3/openapi.json" --appname petstore-swagger
```

Do **not** add `--target`: omitting it enables `swagger-only` mode and ensures
that the analyzer does not call the API. Provide the URL or file path of the
OpenAPI document, not just the URL of a Swagger UI page.

If the command displays the message
`[ERR] Failed to load spec dashboard/sample-swagger.yaml: Cannot parse OpenAPI spec from dashboard/sample-swagger.yaml`,
first check that the analyzer dependencies were installed from the repository
root in Git Bash, using the same Python interpreter as the one used to run the
analyzer:

```bash
python -m pip install -r scripts/requirements.txt
```

Then run the analysis command again.

If you have questions about [scripts/start.sh](../../scripts/start.sh) or its
parameters, see the [HOWTO guide](./HOWTO.md).

### 2.2 Open and discuss the report

Once the analysis is complete, open `dashboard/index.html` in a browser if it
does not open automatically. The generated report is saved to
`reports/latest-report.json`.

Discuss which information can be assessed from the specification and which
measurements require a running API. Results from Swagger-only mode are based
on the contract: they are not actual measurements of response time or payload
size.

---

## Part 3 — Generate a Green Score report for an existing application

Use an application that is already running, whether it is written in Java,
.NET, or Python.

### 3.1 Check that the application and its Swagger specification are accessible

Start the application by following its usual instructions. Before running the
analyzer, identify:

- the application's base URL and a health endpoint or another endpoint that is expected to respond;
- the URL of the Swagger document in JSON or YAML format (for example, `/v3/api-docs`, `/swagger/v1/swagger.json`, or `/openapi.json`).

In Git Bash, check that both URLs respond. Replace the example URLs with those
for your application:

```bash
curl -f "http://localhost:8080/health"
curl -f "http://localhost:8080/v3/api-docs"
```

The health endpoint path depends on the application. If the application or its
Swagger document is protected, make sure you have the necessary permissions
before continuing.

### 3.2 Run the analysis on the application

Provide both the base URL of the running application and the URL of its Swagger
document. Adapt the URLs and application name to your configuration:

```bash
bash scripts/start.sh \
  --target http://localhost:8080 \
  --swagger http://localhost:8080/v3/api-docs \
  --appname my-application
```

The analyzer can now measure the endpoints described in the specification.
Open `dashboard/index.html` in a browser to view the Green Score report
(`reports/latest-report.json`).

---

## Part 4 — Analyze source code with Creedengo

[Creedengo](https://green-code-initiative.org/) complements the previous
analyses: it checks for eco-design rules in **source code** (Java, Python, or
C#). The API Green Score evaluates the Swagger specification and the API's
actual behavior (Part 3). The two analyses produce separate results. The API
does not need to be running for this part.

This part requires Docker or Podman to run SonarQube, as well as a folder or Git
repository containing the source code to analyze. Use the usual
`scripts/start.sh` script with `--creedengo`. The example below analyzes the
sample Swagger specification in `swagger-only` mode with Creedengo. Adjust the
script parameters for your specification and project:

```bash
bash scripts/start.sh \
  --swagger dashboard/sample-swagger.yaml \
  --source-dir samples/java-spring \
  --appname example-java-sample \
  --creedengo
```

You can also try the Java, Python, and .NET projects available in this
repository: [Java](../../samples/java-spring/),
[Python](../../samples/python-fastapi/), and
[.NET](../../samples/csharp-aspnet/). You can also provide an accessible Git
repository; `start.sh` clones it and runs Creedengo (Java 21 example):

```bash
bash scripts/start.sh \
  --swagger dashboard/sample-swagger.yaml \
  --git-repo https://github.com/felix-seifert/java-21-maven-project.git \
  --appname example-java-21 \
  --creedengo
```

Open the dashboard in your browser to review the results, then discuss the
highest-priority findings and possible improvements.

---

## Bonus — CI pipeline

Integrate the analyzer into your project's pipeline (Azure DevOps or GitHub
Actions). See the templates in [`templates/ci`](../../templates/ci) and
[CI-INTEGRATION.md](CI-INTEGRATION.md).

The pipeline (`pr-green-api-axa.yml`):

- runs on **pull requests** and **every week** (on Sunday);
- installs JDK 17+, Maven, and Python;
- clones the analyzer;
- runs `scripts/start.sh` with the specified parameters;
- analyzes Creedengo, Green Score, and OpenAPI.

### Recommendations

| Topic | Checks |
|-------|---------------------------|
| Variables | Check that `TARGETS`, `SWAGGER_URL`, `STACK`, and `BUILD_AND_RUN` are defined. |
| Swagger accessibility | Check that the CI agent can authenticate and get a `200` response from the OpenAPI document. |
| Modules | Check the Maven/Gradle module names and the target subdirectory (`JAVA_MODULE`). |
| Secrets | Store `API_TOKEN`, `CLIENT_SECRET`, etc. in **secret** CI variables, never in the YAML file or logs. |

- [ ] Pipeline added on a separate branch
- [ ] First run completed successfully.
- [ ] Report/dashboard published as an artifact.

---

## General troubleshooting

| Problem | Solution |
|----------|----------|
| `start.sh` does not run | Use Git Bash, which is required for this workshop; do not use PowerShell, Command Prompt, or WSL. |
| Python runtime or dependency missing | Check that Python 3.10+ is installed, then rerun `python -m pip install -r scripts/requirements.txt` from the repository root. |
| Swagger-only analysis cannot load the specification | Check that `--swagger` points to an accessible OpenAPI document in JSON/YAML format or a valid local file. |
| Running application is inaccessible | Check that the application is running and that the base URL and port are correct. |
| OpenAPI document is inaccessible | Check the document URL and authentication requirements, and make sure it returns a successful response. |
| Very low scores across all rules | Check the HTTP status codes in the report; protected endpoints may return `401` or `403`. |
| More information needed | Rerun the analysis with `--debug`. |

---

## Resources

- [Project README](../../README.md) · [HOWTO](HOWTO.md) · [CI integration](CI-INTEGRATION.md)
- [`dashboard/`](../../dashboard): existing dashboard and sample OpenAPI specification
- [**API GreenScore v1.2** scorecard (PDF)](https://cdn.digitevent.com/69243f238739dbd18f49846f/websiteBtnFileUrl/0c90ba15-f0d0-4b1a-9fb4-ebd8dfb1717c-71-48-cat-sustainable-api-greenscore-v1-2.pdf)
- [Sobri-IT](https://sobri-it.axa-fr.intraxa/)
- Workshop slides: see [atelier-project-structure.html](../../atelier-project-structure.html).
