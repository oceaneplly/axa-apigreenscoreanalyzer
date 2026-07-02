# ADR template

Cette bibliothèque fournit **10 Architecture Decision Records** (format MADR)
prêts à copier dans `docs/adr/` de votre projet. Chaque ADR contient un
front-matter YAML **vérifiable automatiquement** par
`scripts/adr_rules.py`.

## Utilisation

```bash
mkdir -p docs/adr
cp templates/adr/*.md docs/adr/
bash scripts/start.sh --source-dir . --adr-dir docs/adr --fail-on-adr-violation
```

## Front-matter — vocabulaire

```yaml
---
adr: 0001                   # numéro unique (4 chiffres)
title: <titre court>
status: accepted            # proposed | accepted | deprecated | superseded
date: 2026-07-02
green_rules: [DE11, AR01]   # règles Green Score liées (info)
verifies:                   # ⇐ vérifications automatiques
  - kind: <checker>
    <param>: <valeur>
---
```

## Checkers disponibles (`kind`)

| `kind`                  | Paramètres attendus                            | Ce que ça vérifie |
|-------------------------|------------------------------------------------|-------------------|
| `has_pagination_params` | `path` (glob), `params` (liste, def. `[page,size]`) | Endpoints de collection déclarent bien les params |
| `sse_endpoint`          | `path` (glob), `content_type` (def. `text/event-stream`) | SSE déclaré dans OpenAPI ET confirmé runtime |
| `absent_query_param`    | `path` (glob), `param`                         | Aucun endpoint ne déclare `param` |
| `cdn_header_present`    | `headers` (liste)                              | ≥ 1 en-tête CDN observé (AR02) |
| `iac_signal`            | `signal` (ex: `hpa`, `keda`, `faas-deps`)      | Signal détecté dans le scan Phase 2 (AR04) |
| `dependency_present`    | `pattern` (regex), `files` (glob, def. build files) | Regex trouvée dans `pom.xml` / `.csproj` / `requirements.txt` |
| `openapi_field`         | `path` (JSONPath simple), `expected` (regex)   | Champ OpenAPI conforme (ex: `info.version` matches `^\d+\.\d+\.\d+$`) |
| `endpoint_returns_status` | `path` (glob), `status` (int)                | Endpoint documenté avec ce status (ex: 429 pour US07) |
| `response_header_present` | `path` (glob), `header` (nom)                | En-tête observé au runtime sur ≥ 1 hit |
| `has_health_endpoint`   | `paths` (liste, def. `/health,/actuator/health,/metrics`) | ≥ 1 endpoint santé exposé |

Les checkers **`iac_signal`** et **`dependency_present`** nécessitent
`--source-dir`. Les autres fonctionnent avec la spec OpenAPI et les
mesures runtime déjà collectées.

