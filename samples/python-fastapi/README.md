# Sample Python FastAPI

## Prérequis
- Python 3.10+

## Démarrer
```bash
pip install -r requirements.txt
uvicorn app:app --port 8000 --reload
# → http://localhost:8000
# OpenAPI: http://localhost:8000/openapi.json
# Swagger UI: http://localhost:8000/docs
```

## Règles couvertes par le workshop

| Règle | Baseline | Après quick-wins |
|---|---|---|
| DE11 pagination | ❌ | ✅ (`page`, `size` params) |
| DE01 GZIP | ❌ | ✅ (`GZipMiddleware`) |
| DE08 fields | ❌ | ✅ (`?fields=`) |
| DE02/03 ETag | ❌ | ✅ (custom middleware) |
| LO01 health | ✅ | ✅ (`/health`) |
| AR01 events | ❌ | ✅ (SSE via `StreamingResponse`) |

