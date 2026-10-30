# 📋 CFP promises → Analyzer capabilities coverage

> Cartographie 1↔1 des promesses du CFP `Axa Summit Workshop CFP.md` vers
> les capacités implémentées dans l'analyzer. Cette matrice est vérifiable
> automatiquement en CI (`scripts/check-promises-coverage.py`).
>
> **Légende** : ✅ implémenté · 🟡 partiel · ❌ manquant

Dernière mise à jour : 2026-07-02

---

## 1. Green Score — règles éco-conception (100 pts)

| Promesse CFP | Règle | ID | Poids | Statut | Composant analyzer |
|---|---|---|---:|---|---|
| Compression GZIP/Brotli | Compression | DE01 | 15 | ✅ | `green-api-auto-discover.py` (probe `Accept-Encoding`) |
| Champs partiels | Field filtering | DE08 | 15 | ✅ | Probe `?fields=` |
| Pagination obligatoire | Pagination | DE11 | 15 | ✅ | Détecte `page/size/limit/offset` |
| Cache ETag / 304 | Cache ETag | DE02/03 | 15 | ✅ | `If-None-Match` probe |
| `/changes` delta sync | Delta | DE06 | 10 | ✅ | Détecte `?since=<ts>` |
| Range / 206 Partial | Range | 206 | 10 | ✅ | Probe `Range: bytes=` |
| Payload binaire | Binary | BIN01 | 10 | 🟡 | Probe `Accept: application/cbor|x-protobuf|msgpack` (à étendre) |
| Observabilité | Health/Metrics | LO01 | 5 | ✅ | Probe `/health`, `/metrics`, `/actuator/health` |
| Rate limiting | 429 | US07 | 5 | ✅ | Détecte `429` + `Retry-After` |

**Total code : 100 pts**

## 2. Architecture & Infrastructure (23 pts)

| Règle | ID | Poids | Statut | Signaux |
|---|---|---:|---|---|
| Event-Driven | AR01 | 6 | ✅ | callbacks OAS · webhooks 3.1 · AsyncAPI · SSE runtime · broker deps |
| Runtime proche | AR02 | 7 | ✅ | CDN headers · TLS handshake · multi-region · GeoIP (opt.) |
| API unique | AR03 | 3 | ✅ | Jaccard signatures · tags · cosine · intra v1/v2 |
| Infra scalable | AR04 | 5 | ✅ | HPA · KEDA · Terraform · Bicep · Serverless · FaaS deps |
| Cloud footprint | AR05 | 2 | ✅ | Provider auto-detect · observability probe · attestation |

**Total architecture : 23 pts** → total workshop = **123 pts**.

## 3. Creedengo static rules (par stack)

| Stack | Statut | Wrapper | Règles clefs (extraits) |
|---|---|---|---|
| Java (Maven/Gradle) | ✅ | plugin SonarQube D1 (`creedengo-java`) | GCI1, GCI3, GCI5, GCI69, GCI72, GCI74, GCI76, GCI77, GCI79, GCI82, GCI94 |
| C# / .NET 8+ | ✅ | D1 (`creedengo-csharp`) sinon fallback D2 stock SQ | GCI69, GCI72, GCI75, GCI81, GCI83, GCI84, GCI85, GCI86, GCI87, GCI88, GCI91, GCI92, GCI93 |
| Python 3.10+ | ✅ | plugin SonarQube D1 (`creedengo-python`) | GCI72, GCI74, GCI89, GCI103, GCI105, GCI109, GCI110, GCI111, GCI112, GCI404 |
| JavaScript / TypeScript | 🟡 | plugin détecté mais non promu dans le CFP | — |
| F# / VB.NET | ❌ | non couvert par Creedengo (warning explicite) | — |

## 4. Pipelines & CI

| Provider | Statut | Fichier |
|---|---|---|
| GitHub Actions | ✅ | `templates/ci/green-score.yml` |
| GitLab CI | ✅ | `docs/CI-INTEGRATION.md` (snippet) |
| Azure DevOps | ✅ | `docs/CI-INTEGRATION.md` (snippet) |
| Threshold gate | ✅ | `green-score-threshold.json` (`minScore`) |
| Badge SVG | ✅ | `badges/green-score.svg` + `scripts/generate-badge.sh` |

## 5. ADR framework (nouveau)

| Capacité | Statut | Fichier |
|---|---|---|
| Format MADR + front-matter YAML | ✅ | `templates/adr/*.md` (10 ADR) |
| Vérification automatique | ✅ | `scripts/adr_rules.py` |
| Intégration dashboard | ✅ | Section "ADR compliance" (radar + table) |
| CI gate (`--fail-on-adr-violation`) | ✅ | flag CLI + exit code |

## 6. Livrables workshop

| Livrable | Statut | Chemin |
|---|---|---|
| Sample app Java Spring Boot | ✅ | `samples/java-spring/` |
| Sample app Python FastAPI | ✅ | `samples/python-fastapi/` |
| Sample app C# ASP.NET Core | ✅ | `samples/csharp-aspnet/` |
| 10 ADR de démarrage | ✅ | `templates/adr/` |
| Workflow GitHub Actions | ✅ | `templates/ci/green-score.yml` |
| Roadmap animateur | ✅ | `docs/WORKSHOP-ROADMAP.md` |
| Dashboard interactif | ✅ | `dashboard/index.html` |
| Badge SVG | ✅ | `badges/green-score.svg` |

---

## 🔄 Régénération

Cette matrice est régénérable via :

```bash
python3 scripts/check-promises-coverage.py > docs/PROMISES-COVERAGE.md
```

Le script échoue (exit ≠ 0) si un des composants marqués ✅ n'existe pas
dans l'arborescence → gate anti-régression documentation.

