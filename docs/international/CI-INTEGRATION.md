# CI Integration — Green Score gate

Three copy-paste-ready snippets to plug the analyzer into your pipeline.

---

## 🐙 GitHub Actions

Copy `templates/ci/green-score.yml` to `.github/workflows/`.

Default config:
- Toolchain **Java 17 + Python 3.11 + .NET 8** (auto-detection via `--stack auto`).
- Local SonarQube startup (ephemeral container).
- Gate `green-score-threshold.json` (`minScore`).
- ADR gate (`--fail-on-adr-violation`).
- Artifact upload + auto-commit of the SVG badge.

---

## 🦊 GitLab CI

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
    - python3 scripts/enforce-threshold.py   # optional helper
  artifacts:
    when: always
    paths:
      - reports/
      - badges/
    expire_in: 30 days
```

---

## 🔷 Azure DevOps

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

---

## 🧪 Local pre-commit hook

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
set -e
bash scripts/start.sh --stack auto --source-dir . \
                      --adr-dir docs/adr --fail-on-adr-violation
```

---

## 🎯 Threshold gate (`green-score-threshold.json`)

```json
{
  "minScore": 85,
  "note": "Below this value, the CI fails."
}
```

Adjust `minScore` according to the maturity of your service:
- **60** — POC / legacy.
- **85** — production service.
- **100+** — critical customer-facing service.
