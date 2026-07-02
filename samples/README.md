# Sample apps

Trois skeletons d'API prêts pour le workshop. Chacun implémente **les mêmes
endpoints** dans son idiome, afin qu'un participant puisse démarrer sur
n'importe quelle stack et suivre exactement le même déroulé.

| Stack | Chemin | Port | Démarrage |
|---|---|---:|---|
| **Java Spring Boot 3** | [`java-spring/`](java-spring/) | 8080 | `mvn spring-boot:run` |
| **Python FastAPI**     | [`python-fastapi/`](python-fastapi/) | 8000 | `uvicorn app:app --port 8000` |
| **C# ASP.NET Core 8**  | [`csharp-aspnet/`](csharp-aspnet/) | 5050 | `dotnet run --urls http://+:5050` |

## Endpoints exposés (mêmes pour les 3 stacks)

| Méthode | Chemin | But / règle |
|---|---|---|
| GET | `/health`             | Health-check (LO01) |
| GET | `/items`              | Collection **sans** pagination (KO au baseline pour DE11) |
| GET | `/items/{id}`         | Single resource — support ETag à ajouter (DE02/03) |
| GET | `/items/events`       | À transformer en SSE (AR01) — au baseline c'est du polling |
| GET | `/items/changes`      | Delta sync `?since=<ts>` (DE06) |
| POST | `/items`             | Mutation sans callback (opportunité AR01) |

Ces skeletons sont **volontairement imparfaits** pour laisser aux
participants de vrais quick-wins à appliquer pendant l'atelier.

