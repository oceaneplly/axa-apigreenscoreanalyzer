# Sample Java Spring Boot 3

## Prérequis
- JDK 17+
- Maven 3.8+

## Démarrer
```bash
mvn spring-boot:run
# → http://localhost:8080
# OpenAPI: http://localhost:8080/v3/api-docs
# Swagger UI: http://localhost:8080/swagger-ui/index.html
# Actuator: http://localhost:8080/actuator/health
```

## Utilisé dans le workshop pour illustrer

| Règle | Baseline | Après quick-wins |
|---|---|---|
| DE11 pagination | ❌ | ✅ (`?page` + `?size`) |
| DE01 GZIP | ❌ | ✅ (`server.compression.enabled=true`) |
| DE08 fields | ❌ | ✅ (query param + jackson filter) |
| DE02/03 ETag | ❌ | ✅ (`ShallowEtagHeaderFilter`) |
| LO01 health | ✅ | ✅ (`/actuator/health`) |
| AR01 events | ❌ (polling) | ✅ (SSE `text/event-stream`) |

