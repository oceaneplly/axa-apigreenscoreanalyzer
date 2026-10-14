# 🌱 HOW-TO — Utiliser l'AXA API Green Score Analyzer de A à Z

Ce guide s'adresse à **tout nouvel utilisateur** (débutant compris) qui veut
lancer l'analyzer :

- **en local (CLI)** — sur son poste,
- **en GitHub Actions**,
- **en Azure DevOps Pipeline**,
- **en GitLab CI**,
- ou via l'**UI interactive** / le **binaire autonome** / le **conteneur Docker**.

> 💡 **En une phrase** : le point d'entrée principal est
> [`scripts/start.sh`](../scripts/start.sh). Il orchestre TOUT
> (build de l'app, health-check, mesure Green Score, analyse éco-conception
> Creedengo, badge SVG, dashboard HTML, gate ADR). Tous les autres scripts sont
> des briques appelées par `start.sh` — mais vous pouvez aussi les lancer seuls.

---

## 📑 Sommaire

1. [Prérequis](#1-prérequis)
2. [Démarrage rapide (30 secondes)](#2-démarrage-rapide-30-secondes)
3. [`start.sh` — le point d'entrée principal](#3-startsh--le-point-dentrée-principal)
   - [Tous les flags](#31-tous-les-flags-de-startsh)
   - [Variables d'environnement](#32-variables-denvironnement)
   - [Recettes CLI courantes](#33-recettes-cli-courantes)
4. [Les autres points d'entrée](#4-les-autres-points-dentrée)
   - [Analyse Green Score seule](#41-green-score-seul)
   - [Analyse Creedengo seule](#42-creedengo-seul)
   - [Lint OpenAPI hors-ligne](#43-lint-openapi-hors-ligne)
   - [UI interactive (serveur local)](#44-ui-interactive)
   - [Binaires autonomes](#45-binaires-autonomes)
   - [Conteneur Docker](#46-conteneur-docker)
   - [Dashboard & badge](#47-dashboard--badge)
   - [Envoi vers SobriIT](#48-envoi-vers-sobriit)
   - [Installer dans un autre repo](#49-installer-dans-un-autre-repo)
5. [Intégration CI/CD](#5-intégration-cicd)
   - [GitHub Actions](#51-github-actions)
   - [Azure DevOps](#52-azure-devops)
   - [GitLab CI](#53-gitlab-ci)
   - [Pre-commit hook](#54-pre-commit-hook-local)
6. [Comprendre les résultats](#6-comprendre-les-résultats)
7. [Dépannage (FAQ)](#7-dépannage-faq)

---

## 1. Prérequis

| Besoin | Détail |
|--------|--------|
| **Bash** | Requis. Sous Windows, utiliser **Git Bash** ou **WSL** (pas PowerShell directement pour `start.sh`). |
| **Python** | 3.10+ avec `pip`. Installer les deps : `pip install -r scripts/requirements.txt`. |
| **Java** (si stack Java) | JDK 17+ et Maven 3.8+ (ou le wrapper `./mvnw` du projet). |
| **.NET** (si stack C#) | .NET SDK 8.0+ (`dotnet --version` ≥ 8). |
| **Container runtime** | Docker **ou** Podman — requis uniquement pour Creedengo (SonarQube). |
| **curl, git** | Utilisés pour les health-checks et le clonage de repo. |

> ℹ️ `start.sh` **auto-installe** Maven / .NET SDK localement (sans sudo) si
> absents, et détecte automatiquement Docker ou Podman.

---

## 2. Démarrage rapide (30 secondes)

Vous avez déjà une API qui tourne sur `http://localhost:8080` :

```bash
# 1. Installer les dépendances Python (une seule fois)
pip install -r scripts/requirements.txt

# 2. Analyser l'API (Green Score uniquement)
bash scripts/start.sh --target http://localhost:8080
```

Résultats produits :
- `reports/latest-report.json` — rapport détaillé,
- `badges/green-score.svg` — badge de score,
- `dashboard/index.html` — dashboard interactif, ouvert automatiquement dans le
  navigateur par `start.sh` en exécution locale.

---

## 3. `start.sh` — le point d'entrée principal

`start.sh` enchaîne, dans l'ordre :

1. **(optionnel) Clone Git** (`--git-repo`) ou utilisation d'un dossier local (`--source-dir`).
2. **(optionnel) Build & run** de l'API en local (`--build-and-run`).
3. **Health-check** des cibles (`/actuator/health`, `/health`, `/`…).
4. **Découverte OpenAPI + mesure** → **Green Score** (100 pts).
5. **Règles d'architecture** AR01–AR05 (+23 pts) et **gate ADR**.
6. **(optionnel) Creedengo** — analyse éco-conception du code (`--creedengo`).
7. **(optionnel) Envoi SobriIT** (`--send-to-sobriit`).
8. **Badge SVG + dashboard HTML**.

### 3.1 Tous les flags de `start.sh`

| Flag | Effet |
|------|-------|
| `--target <url>` | URL d'une API à analyser. **Répétable**. |
| `--targets <csv>` | Liste d'URLs séparées par virgules (`http://a:8080,http://b:8082`). |
| `--swagger <url\|file>` | Spec OpenAPI explicite (sinon auto-découverte). Répétable. |
| `--swaggers <csv>` | Liste de specs séparées par virgules. |
| `--bearer <token>` | Bearer token pour endpoints protégés. |
| `--appname <name>` | Nom de l'application dans les rapports (défaut : nom du dossier). |
| `--stack <auto\|java\|dotnet>` | Force le stack ; `auto` détecte depuis `--source-dir`. |
| `--source-dir <path>` | Dossier du code source local (build, AR01/AR04, Creedengo). |
| `--build-and-run` | Compile **et** démarre l'API avant l'analyse. Exige `--source-dir`. |
| `--creedengo` | Active l'analyse éco-conception Creedengo (nécessite Docker/Podman). |
| `--git-repo <url>` | Clone un repo distant (source unique build + Creedengo). Implique `--creedengo`. |
| `--git-branch <b>` | Branche/tag à checkout. |
| `--git-subdir <p>` | Analyser un sous-dossier du repo cloné. |
| `--git-keep` | Conserver le clone après analyse (sinon supprimé). |
| `--root <path>` | Dossier projet explicite pour Creedengo. |
| `--adr-dir <path>` | Dossier des ADR à vérifier (défaut : `docs/adr`). |
| `--fail-on-adr-violation` | Fait échouer le build si un ADR `status: accepted` échoue. |
| `--consumer-region <ISO2>` | Région des consommateurs (AR02, ex. `FR`, `US`). |
| `--enable-geoip` | Active la vérif GeoIP (ipinfo.io) pour AR02 anycast/ASN. |
| `--cloud-footprint-confirmed` | Atteste l'usage du dashboard carbone cloud (valide AR05). |
| `--send-to-sobriit` | Envoie les résultats vers la plateforme SobriIT. |
| `--app-code <code>` | Code applicatif SobriIT. |
| `--debug` | Mode verbeux. |

> 🔁 Les flags acceptent aussi la forme `--flag=valeur` pour `--stack`,
> `--source-dir`, `--consumer-region`, `--adr-dir`.

### 3.2 Variables d'environnement

Alternatives aux flags (pratiques en CI) :

| Variable | Équivalent flag |
|----------|-----------------|
| `BEARER_TOKEN` | `--bearer` |
| `APPNAME` | `--appname` |
| `CONSUMER_REGION` | `--consumer-region` |
| `ENABLE_GEOIP=true` | `--enable-geoip` |
| `CLOUD_FOOTPRINT_CONFIRMED=true` | `--cloud-footprint-confirmed` |
| `ADR_DIR` | `--adr-dir` |
| `FAIL_ON_ADR_VIOLATION=true` | `--fail-on-adr-violation` |
| `SOBRIIT_APP_CODE` | `--app-code` |
| `SOBRIIT_BASE_URL`, `SOBRIIT_API_KEY`, `SOBRIIT_APP_DSI`, `SOBRIIT_APP_TRIBE`, `SOBRIIT_APP_TRIBE_ID` | Config SobriIT |
| `JAVA_MODULE` | Force le sous-module Maven à lancer (multi-module). |
| `LOMBOK_VERSION` | Force la version Lombok patchée pour le build Java. |
| `SONAR_PORT` | Port SonarQube Creedengo (défaut : 9100). |

### 3.3 Recettes CLI courantes

```bash
# ── API déjà démarrée, Green Score seul ─────────────────────────────
bash scripts/start.sh --target http://localhost:8080

# ── Plusieurs APIs en une passe ─────────────────────────────────────
bash scripts/start.sh --targets http://localhost:8080,http://localhost:8082

# ── Endpoints protégés (bearer token) ───────────────────────────────
bash scripts/start.sh --target http://localhost:8080 --bearer "eyJhbGciOi..."
# ou :
BEARER_TOKEN=eyJhbGciOi... bash scripts/start.sh --target http://localhost:8080

# ── Java : build + run automatique + Creedengo ──────────────────────
bash scripts/start.sh --stack java --build-and-run \
                      --source-dir ./my-spring-app --creedengo

# ── .NET : build + run automatique + Creedengo ──────────────────────
bash scripts/start.sh --stack dotnet --build-and-run \
                      --source-dir ./MyAspNetApi --creedengo \
                      --target http://localhost:5050

# ── Auto-détection du stack depuis le dossier source ────────────────
bash scripts/start.sh --stack auto --source-dir . --build-and-run --creedengo

# ── Analyser un repo distant sans copie locale ──────────────────────
bash scripts/start.sh --git-repo https://github.com/org/repo.git \
                      --git-branch main --creedengo

# ── Gate ADR (fait échouer si un ADR "accepted" n'est pas respecté) ─
bash scripts/start.sh --source-dir . --adr-dir docs/adr --fail-on-adr-violation

# ── Scoring architecture complet (AR02 + AR05) ──────────────────────
bash scripts/start.sh --target http://localhost:8080 \
                      --consumer-region FR --enable-geoip \
                      --cloud-footprint-confirmed

# ── Tout activer + envoi SobriIT ────────────────────────────────────
bash scripts/start.sh --stack auto --source-dir . --build-and-run \
                      --creedengo --adr-dir docs/adr --fail-on-adr-violation \
                      --send-to-sobriit --app-code MYAPP
```

> ⚠️ **Chemins avec espaces** : mettez-les entre guillemets →
> `--source-dir "/chemin/avec espaces/projet"`.

---

## 4. Les autres points d'entrée

Tous ces scripts sont appelés par `start.sh`, mais restent utilisables seuls.

### 4.1 Green Score seul

Wrapper de découverte + mesure (sans Creedengo, sans build) :

```bash
# Via variables d'environnement
TARGET_URL=http://localhost:8080 \
  bash scripts/green-score-analyzer_withdiscovery.sh --debug
```

Ou directement le moteur Python (le plus flexible) :

```bash
python3 scripts/green-api-auto-discover.py \
  --target http://localhost:8080 \
  --swagger http://localhost:8080/v3/api-docs \
  --appname my-api \
  --repeat 3 \
  --methods get,post \
  --output-dir reports/
```

Flags utiles de `green-api-auto-discover.py` :

| Flag | Effet |
|------|-------|
| `--target <url>` | Base URL de l'API (répétable ou CSV). |
| `--swagger <url\|file>` | Spec OpenAPI (répétable ou CSV). |
| `--bearer <token>` | Authentification. |
| `--param key=value` | Paramètre de path/query injecté (répétable). |
| `--repeat <n>` | Nombre de mesures par endpoint (défaut : 3). |
| `--methods <csv>` | Méthodes HTTP (défaut : get,post,put,patch,delete). |
| `--dry-run` | Liste les endpoints sans les appeler. |
| `--source-dir <path>` | Code source (AR01/AR04). |
| `--adr-dir <path>` | Dossier ADR (auto-détecté : `./docs/adr` ou `./adr`). |
| `--fail-on-adr-violation` | Exit ≠ 0 si un ADR échoue. |
| `--consumer-region <code>` / `--enable-geoip` | AR02. |
| `--cloud-footprint-confirmed` | AR05. |
| `--output-dir <dir>` | Dossier de sortie (défaut : `reports/`). |

### 4.2 Creedengo seul

Analyse éco-conception statique du **code source** (Java / Python / C#) via
SonarQube + plugin Creedengo (nécessite Docker/Podman) :

```bash
# Dossier local
bash scripts/creedengo-analyzer.sh --root ./my-app --lang java

# Repo distant
bash scripts/creedengo-analyzer.sh \
  --git-repo https://github.com/org/repo.git --git-branch main --lang csharp
```

| Flag | Effet |
|------|-------|
| `--root <path>` | Dossier projet (défaut : dossier courant). |
| `--lang <java\|python\|csharp\|dotnet>` | Force le langage. |
| `--git-repo/--git-branch/--git-subdir/--git-keep` | Clonage Git. |
| `--skip-build` | Ne pas recompiler. |
| `--no-cleanup` | Laisse SonarQube tourner (accessible sur `http://localhost:9100`). |
| `--force-cleanup` | Détruit containers/volumes/images SonarQube. |
| `--skip-dashboard` | Ne pas régénérer le dashboard. |
| `--debug` | Verbeux. |

Sortie : `reports/creedengo-report.json`.

### 4.3 Lint OpenAPI hors-ligne

Vérifie les règles Green API **statiques** sur une spec, **sans appeler l'API**
(idéal en CI rapide / pre-commit) :

```bash
python3 scripts/green-api-lint.py openapi.yaml --format text
python3 scripts/green-api-lint.py openapi.yaml --format json  --fail-on-warn
python3 scripts/green-api-lint.py openapi.yaml --format sarif > lint.sarif
```

Codes de sortie : `0` = OK · `1` = findings (+ `--fail-on-warn`) · `2` = fichier invalide.

### 4.4 UI interactive

Dashboard web local pour lancer les analyses depuis un navigateur :

```bash
bash scripts/start-interactive.sh              # http://127.0.0.1:8765
bash scripts/start-interactive.sh --port 9000 --no-open
```

En interne il lance `greenapianalyzer-server.py` qui expose :

- `GET /` → l'UI (`dashboard/interactive.html`),
- `POST /api/discover` → découverte des specs OpenAPI des cibles,
- `POST /api/analyze` → lance l'analyse et renvoie `latest-report.json`.

Onglet **« Local Green Score / Creedengo Source analyse »** : sélecteur de
stack, dossier source, checkbox build & run, console live des logs.

### 4.5 Binaires autonomes

Pour distribuer l'outil sans dépendances :

```bash
# Binaire complet (analyze + lint + serve)
bash scripts/build-binary.sh --output dist/greenanalyzer

# Utilisation
dist/greenanalyzer analyze --target http://localhost:8080
dist/greenanalyzer lint openapi.yaml
dist/greenanalyzer serve --port 8765

# Binaire léger (lint OpenAPI uniquement, ~20 KB)
bash scripts/build-lint-binary.sh --output dist/green-api-lint
dist/green-api-lint openapi.yaml --format json
```

### 4.6 Conteneur Docker

L'image embarque Python, Spectral, curl, jq et tous les scripts.
L'`ENTRYPOINT` est le moteur `green-api-auto-discover.py` :

```bash
# Build
docker build -t greenanalyzer .

# Analyser une API (les args sont passés à l'analyzer)
docker run --rm greenanalyzer --target http://host.docker.internal:8080

# Lint d'une spec montée en volume
docker run --rm -v "$PWD:/work" greenanalyzer \
  lint /work/openapi.yaml --format json
```

### 4.7 Dashboard & badge

Régénérer manuellement à partir d'un rapport existant :

```bash
# Dashboard HTML + Markdown
bash scripts/generate-dashboard.sh reports/latest-report.json \
     dashboard/index.save.html dashboard/index.html reports/creedengo-report.json

# Badge SVG
bash scripts/generate-badge.sh reports/latest-report.json badges/green-score.svg
```

### 4.8 Envoi vers SobriIT

Directement (sans repasser par `start.sh`) :

```bash
python3 scripts/sobriit_sender.py \
  --appname my-api \
  --green-report reports/latest-report.json \
  --creedengo-report reports/creedengo-report.json \
  --app-code MYAPP
```

Config via env : `SOBRIIT_BASE_URL`, `SOBRIIT_API_KEY`, `SOBRIIT_APP_CODE`,
`SOBRIIT_APP_DSI`, `SOBRIIT_APP_TRIBE`, `SOBRIIT_APP_TRIBE_ID`.

### 4.9 Installer dans un autre repo

`installer.sh` clone un repo cible, crée une branche et y copie tout l'outillage
(scripts, dashboard, badges, `.creedengo/`, workflow GitHub, `.spectral.yml`,
`green-score-threshold.json`) :

```bash
bash installer.sh https://github.com/org/mon-api.git
```

---

## 5. Intégration CI/CD

Le principe est **identique partout** : installer les toolchains → (option)
démarrer SonarQube → lancer `start.sh` → gate sur `green-score-threshold.json`
→ publier `reports/` et `badges/`.

Le fichier `green-score-threshold.json` définit le score minimal :

```json
{ "minScore": 85, "note": "En dessous, la CI échoue." }
```

Barème conseillé : **60** (POC/legacy) · **85** (production) · **100+** (critique).

### 5.1 GitHub Actions

Copiez [`templates/ci/green-score.yml`](../templates/ci/green-score.yml) dans
`.github/workflows/` de votre repo. Il fait déjà tout :

- Setup **JDK 17 + Python 3.11 + .NET 8**,
- Démarre un SonarQube éphémère,
- Lance `start.sh --stack auto --source-dir . --build-and-run --creedengo --adr-dir docs/adr --fail-on-adr-violation`,
- Applique le gate `green-score-threshold.json`,
- Upload `reports/` + `badges/`,
- Commit automatiquement le badge SVG sur `main`.

Seule config requise : le secret **`API_BEARER_TOKEN`** (si votre API est protégée).

Extrait clé :

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

> 🔐 Définissez `API_BEARER_TOKEN` dans **Pipelines → Library** (variable secrète).

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
# Rapide : lint OpenAPI hors-ligne (pas besoin d'app démarrée)
python3 scripts/green-api-lint.py openapi.yaml --fail-on-warn

# OU complet : gate ADR + Green Score
bash scripts/start.sh --stack auto --source-dir . \
                      --adr-dir docs/adr --fail-on-adr-violation
```

---

## 6. Comprendre les résultats

| Fichier | Contenu |
|---------|---------|
| `reports/latest-report.json` | Rapport Green Score complet (100 pts code + 23 archi). |
| `reports/creedengo-report.json` | Findings éco-conception (règles GCI). |
| `reports/discovered-openapi.json` | Specs OpenAPI fusionnées des cibles. |
| `badges/green-score.svg` | Badge de score (à embarquer dans un README). |
| `dashboard/index.html` | Dashboard interactif (ouvrir dans un navigateur). |
| `dashboard/index.md` | Version Markdown du dashboard. |

Le **score total est sur 123 pts** : 100 pts de règles code (pagination DE11,
filtrage DE08, gzip DE01, cache ETag DE02/03, delta DE06, range 206, format
binaire, observabilité LO01, rate-limit US07) + 23 pts d'architecture
(événementiel AR01, proximité runtime AR02, single API AR03, scalabilité AR04,
empreinte cloud AR05).

---

## 7. Dépannage (FAQ)

| Symptôme | Solution |
|----------|----------|
| **`start.sh` ne se lance pas sous Windows** | Utilisez **Git Bash** ou **WSL** (pas PowerShell/cmd). |
| **Timeout « cibles non prêtes »** | L'API n'a pas répondu sur `/health`/`/actuator/health`/`/`. Vérifiez l'URL et le port ; augmentez le temps de démarrage. |
| **`--build-and-run` : stack non détecté** | Précisez `--stack java` ou `--stack dotnet`. Indices cherchés : `pom.xml`, `build.gradle`, `*.csproj`, `*.sln`. |
| **Java multi-module : mauvais module lancé** | Forcez avec `JAVA_MODULE=<nom-du-module>`. |
| **Erreurs Lombok à la compilation** | `LOMBOK_VERSION=1.18.34 bash scripts/start.sh …` (patch auto dans un checkout jetable). |
| **Creedengo ne démarre pas** | Docker/Podman requis. SonarQube tourne sur `http://localhost:9100` (paramétrable via `SONAR_PORT`). |
| **Endpoints protégés → 401** | Fournissez `--bearer <token>` ou `BEARER_TOKEN=…`. |
| **C# : prompt dev-cert HTTPS** | On force `ASPNETCORE_URLS=http://+:<port>` (HTTP) pour éviter le prompt. |
| **Premier `dotnet restore` très lent** | Cache NuGet vide — normal la 1re fois (timeout étendu). |
| **Mono-repo Java + .NET** | Utilisez `--stack` explicite pour lever l'ambiguïté. |

---

📚 Voir aussi :
[README](../README.md) ·
[CI-INTEGRATION](./CI-INTEGRATION.md) ·
[ADR templates](../templates/adr/) ·
[Sample apps](../samples/).
