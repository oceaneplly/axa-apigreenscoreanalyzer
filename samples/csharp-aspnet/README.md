# Sample C# ASP.NET Core 8

## Prérequis
- .NET SDK 8.0+

## Démarrer
```bash
dotnet run --urls http://+:5050
# → http://localhost:5050
# OpenAPI: http://localhost:5050/swagger/v1/swagger.json
# Swagger UI: http://localhost:5050/swagger
```

## Règles couvertes par le workshop

| Règle | Baseline | Après quick-wins |
|---|---|---|
| DE11 pagination | ❌ | ✅ (`page`, `size` query) |
| DE01 GZIP | ❌ | ✅ (`AddResponseCompression`) |
| DE08 fields | ❌ | ✅ (`?fields=`) |
| DE02/03 ETag | ❌ | ✅ (`Marvin.Cache.Headers`) |
| LO01 health | ✅ | ✅ (`/health`) |
| AR01 events | ❌ | ✅ (SSE via `ContentType=text/event-stream`) |

