# 🗺️ Workshop Roadmap — Green Architecture

> Rejouable par n'importe quel animateur. Deux formats : **2 h (Summit)** et
> **3 h (workshop indépendant)**. Stacks : **Java · Python · C#** (au choix
> du participant, aucun code de glue à écrire).

---

## 🎯 Objectifs pédagogiques

À la fin du workshop, chaque participant est capable de :

1. Mesurer le **Green Score** (code + architecture) d'une API existante.
2. Appliquer 5 quick-wins qui remontent le score de +30 à +40 points.
3. Documenter les décisions d'architecture verte via des **ADR** vérifiés
   automatiquement en CI.
4. Brancher le tout dans **Votre CI/CD** avec un gate anti-régression.

---

## ✅ Pré-requis participants

- **Git** + éditeur (VS Code / IntelliJ / Rider).
- **Docker Desktop** ou **Podman** (SonarQube local).
- Une des trois stacks au choix :
  - Java 17+ + Maven 3.8+
  - Python 3.10+
  - .NET SDK 8.0+
- ~10 Go de disque libre (images Docker + NuGet/Maven cache).

Kit à cloner **avant** le workshop :

```bash
git clone https://github.com/<org>/axa-apigreenscoreanalyzer.git
cd axa-apigreenscoreanalyzer
bash installer.sh           # installe les deps, warmup Docker
```

---

## ⏱️ Format court — 2 h (Summit "hands-on" slot)

| # | Durée | Bloc | Contenu | Livrable / Checkpoint |
|---|-------|------|---------|-----------------------|
| 0 | 5 min | **Kickoff** | Contexte green IT · chiffres clefs (empreinte IT ~4 % CO₂e mondial) · objectifs du workshop | — |
| 1 | 15 min | **Setup** | Clone, `bash installer.sh`, choix de la stack (Java/Python/C#), démarrage sample app (`samples/<stack>/`) | App UP sur port 8080/8000/5050 |
| 2 | 20 min | **Act 1 — Measure** | `bash scripts/start.sh --target http://localhost:<port> --source-dir samples/<stack>` → dashboard baseline | Score baseline visible dans `reports/latest-report.json` |
| 3 | 25 min | **Act 2 — Code quick-wins** | Appliquer 5 fixes : DE11 pagination · DE01 GZIP · DE08 `fields` · DE02/03 ETag · DE06 `/changes` | Score global **+30 pts** minimum |
| 4 | 25 min | **Act 3 — Architecture** | AR01 SSE au lieu de polling · AR03 dédup v1/v2 · AR04 exemple HPA/serverless · AR05 provider dashboard | ≥ 3 règles AR* passent à ✅ |
| 5 | 15 min | **ADR gate** | Ajouter 3 ADR (`docs/adr/`), faire échouer volontairement 1 ADR, réparer | `reports/adr-report.json` OK |
| 6 | 10 min | **CI wiring** | Copier `.github/workflows/green-score.yml`, push, observer le run + badge | Workflow vert + badge SVG mis à jour |
| 7 | 5 min | **Wrap-up** | Q&A · ressources · roadmap OSS Creedengo & API Green Score | — |

---

## ⏱️ Format long — 3 h (workshop indépendant)

Reprend le format court + 3 blocs additionnels de 30 min :

| # | Durée | Bloc | Contenu | Livrable |
|---|-------|------|---------|----------|
| 3-bis | 30 min | **BIN01 & payload binaire** | Ajouter un endpoint `Accept: application/cbor` (ex. via `cbor2`, `Jackson-CBOR`, `MessagePack`) et mesurer la réduction de payload | −40 % à −60 % de bytes |
| 4-bis | 30 min | **AR02 avancé** | `--consumer-region FR --enable-geoip` · lecture des TLS handshake · plan multi-région | AR02 = 7/7 |
| 6-bis | 30 min | **Coaching par stack (breakouts)** | Groupes Java / Python / C# — l'animateur passe voir chaque table | Score personnel par participant |

---

## 🎬 Détail des Actes

### Act 1 — Measure

**Commandes**

```bash
# Stack au choix — le script auto-détecte
bash scripts/start.sh \
     --stack auto \
     --source-dir samples/java-spring \
     --build-and-run \
     --creedengo
```

**Ce que le participant doit voir dans le dashboard :**
- Score global sur 123 pts.
- Bandeau "Architecture 23" **au même niveau** que "Code 100".
- Radar chart AR01→AR05.
- Table endpoint-par-endpoint avec bytes / latence / cache / ETag.

### Act 2 — Code quick-wins (Creedengo + rules)

Ordre recommandé (impact décroissant) :

1. **DE11 pagination** — ajouter `?page`/`?size` sur les collections. +15 pts.
2. **DE01 compression** — middleware GZIP (Spring/FastAPI/ASP.NET). +15 pts.
3. **DE08 fields** — filtre `?fields=id,name`. +15 pts.
4. **DE02/03 ETag** — hash de payload + 304 sur `If-None-Match`. +15 pts.
5. **DE06 delta** — endpoint `/changes?since=<ts>`. +10 pts.

Puis relancer :

```bash
bash scripts/start.sh --target http://localhost:<port> --source-dir samples/<stack>
```

### Act 3 — Architecture (le "gap" à combler dans la plupart des APIs)

- **AR01** — supprimer le polling `/changes` et exposer un `/events` en SSE
  (`text/event-stream`). Voir ADR `0007`.
- **AR03** — repérer les doublons `v1/v2` détectés par le rapport, marquer
  la v1 comme `deprecated`.
- **AR04** — ajouter un exemple HPA (`k8s/hpa.yaml`) OU un `serverless.yml`.
  Le scan Phase 2 (`--source-dir`) doit le détecter.
- **AR05** — activer `--cloud-footprint-confirmed` OU exposer `/metrics`.

### Act 4 — ADR gate

1. Copier les 10 ADR fournis depuis `templates/adr/` vers `docs/adr/`.
2. Lancer :
   ```bash
   bash scripts/start.sh --source-dir . --adr-dir docs/adr --fail-on-adr-violation
   ```
3. Modifier volontairement un endpoint pour casser l'ADR `0002-pagination`
   (retirer `?page`). Le CI doit **échouer**.
4. Réparer → CI vert.

### Act 5 — CI wiring

```bash
mkdir -p .github/workflows
cp templates/ci/green-score.yml .github/workflows/
git add . && git commit -m "chore: green-score CI gate"
git push
```

Puis :
- Onglet **Actions** GitHub → le run doit être vert.
- `badges/green-score.svg` mis à jour et affiché dans le README.

---

## 👨‍🏫 Guide animateur — Checkpoints & fallbacks

À la fin de chaque Act, l'animateur vérifie :

| Checkpoint | Fichier à vérifier | Fallback si KO |
|---|---|---|
| Act 1 baseline | `reports/latest-report.json` existe et contient `total_score` | Vérifier que l'app est bien UP (`curl :port/health`) |
| Act 2 quick-wins | `total_score` a augmenté de ≥ 30 pts | Reprendre DE11 pas-à-pas (le plus visuel) |
| Act 3 architecture | ≥ 3 règles AR* avec `matched: true` | Utiliser `--cloud-footprint-confirmed` + copier `k8s/hpa.yaml` fourni |
| Act 4 ADR | `reports/adr-report.json` avec ≥ 1 fail puis pass | Reprendre l'exemple `0002-pagination` |
| Act 5 CI | Run GitHub Actions ✅ | Fallback local : `act` (nektos/act) |

---

## 📚 Ressources fournies (dans le repo)

- `templates/adr/` — 10 ADR de démarrage.
- `templates/ci/green-score.yml` — workflow GitHub Actions.
- `samples/java-spring/` · `samples/python-fastapi/` · `samples/csharp-aspnet/`
- `docs/PROMISES-COVERAGE.md` — matrice promesses ↔ règles.
- `docs/CI-INTEGRATION.md` — snippets GitLab CI + Azure DevOps.

---

## 🔗 Liens externes

- API Green Score framework : https://github.com/AXA-GROUP-OPERATIONS/api-green-score
- Creedengo (ex-ecoCode) : https://github.com/green-code-initiative
- Spectral : https://stoplight.io/open-source/spectral
- SonarQube : https://www.sonarsource.com/products/sonarqube/

