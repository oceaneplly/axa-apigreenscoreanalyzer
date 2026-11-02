# 🌿 Green API Score Dashboard

> 📦 **Application : example-java-sample**
>
> **Summit AXA 2026 — Green Architecture : moins de gras, plus d'impact !**

📅 *Dernière analyse : 2026-11-02T10:45:07Z*

---

## 🔴 Green Score : **18/100** — Grade **E** 📉

### 📋 Détail par règle

| Statut | Règle | Score | Max | Endpoints | Détail |
|:------:|-------|------:|----:|:---------:|--------|
| ✅ | DE11 Pagination | 15 | 15 | 1/1 | Pagination on 1/1 collection endpoint(s) |
| ❌ | DE08 Filtrage champs | 0 | 15 | 0/2 | No field filter found |
| ❌ | DE01 Compression | 0 | 15 | 0/2 | Neither gzip nor brotli detected |
| ❌ | DE02/03 Cache ETag | 0 | 15 | 0/1 | ETag/304 not detected |
| ❌ | DE06 Delta | 0 | 10 | 0/2 | No delta endpoint found |
| ❌ | 206 Range | 0 | 10 | 0/2 | Range not supported |
| ❌ | LO01 Observabilité | 0 | 5 | 0/5 | No health endpoint |
| ❌ | US07 Rate Limit | 0 | 5 | 0/2 | Cannot verify |
| ❌ | AR02 CBOR | 0 | 10 | 0/2 | No binary format endpoint (spec + runtime probes empty) |


---

## 🏛️ Architecture : **3/23** 🔴

> **Ces règles pèsent 23 points** — au même titre que les règles code — mais sont souvent oubliées. Elles portent sur la topologie de l'API (événements, edge/CDN, dédup, autoscaling, empreinte cloud).

<svg xmlns="http://www.w3.org/2000/svg" width="260" height="260" viewBox="0 0 260 260"><polygon points="130.0,105.0 153.8,122.3 144.7,150.2 115.3,150.2 106.2,122.3" fill="none" stroke="#e5e7eb" stroke-width="1"/><polygon points="130.0,80.0 177.6,114.5 159.4,170.5 100.6,170.5 82.4,114.5" fill="none" stroke="#e5e7eb" stroke-width="1"/><polygon points="130.0,55.0 201.3,106.8 174.1,190.7 85.9,190.7 58.7,106.8" fill="none" stroke="#e5e7eb" stroke-width="1"/><polygon points="130.0,30.0 225.1,99.1 188.8,210.9 71.2,210.9 34.9,99.1" fill="none" stroke="#e5e7eb" stroke-width="1"/><line x1="130.0" y1="130.0" x2="130.0" y2="30.0" stroke="#d1d5db" stroke-width="1"/><line x1="130.0" y1="130.0" x2="225.1" y2="99.1" stroke="#d1d5db" stroke-width="1"/><line x1="130.0" y1="130.0" x2="188.8" y2="210.9" stroke="#d1d5db" stroke-width="1"/><line x1="130.0" y1="130.0" x2="71.2" y2="210.9" stroke="#d1d5db" stroke-width="1"/><line x1="130.0" y1="130.0" x2="34.9" y2="99.1" stroke="#d1d5db" stroke-width="1"/><polygon points="130.0,130.0 130.0,130.0 188.8,210.9 130.0,130.0 130.0,130.0" fill="rgba(34,197,94,0.35)" stroke="#16a34a" stroke-width="2"/><text x="130.0" y="15.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="#374151">AR01 (0/6)</text><text x="239.4" y="94.5" text-anchor="start" font-size="11" font-family="sans-serif" fill="#374151">AR02 (0/7)</text><text x="197.6" y="223.0" text-anchor="start" font-size="11" font-family="sans-serif" fill="#374151">AR03 (3/3)</text><text x="62.4" y="223.0" text-anchor="end" font-size="11" font-family="sans-serif" fill="#374151">AR04 (0/5)</text><text x="20.6" y="94.5" text-anchor="end" font-size="11" font-family="sans-serif" fill="#374151">AR05 (0/2)</text></svg>

| Statut | Règle | Score | Max | Signaux détectés |
|:------:|-------|------:|----:|------------------|
| ❌ | **AR01** Event-Driven Architecture | 0 | 6 | — |
| ❌ | **AR02** Runtime proche du consommateur | 0 | 7 | tls_skip |
| ✅ | **AR03** Une seule API par besoin | 3 | 3 | info |
| ❌ | **AR04** Infrastructure scalable | 0 | 5 | — |
| ❌ | **AR05** Cloud footprint dashboard | 0 | 2 | — |

### 📊 Mesures par endpoint (API découverte)

| Méthode | Endpoint | Taille | Temps | HTTP |
|:-------:|----------|-------:|------:|-----:|
| GET | `/books` | 0 B | 0.000s | 0 |
| GET | `/books/{id}` | 0 B | 0.000s | 0 |

### 🔑 Métriques clés

- **Endpoints mesurés** : 2
- **Transfert total** : 0 B
- **Transfert moyen / endpoint** : 0 B
- **Temps moyen** : 0.000s
- **⚡ Énergie totale / appel** : 0.0000 Wh
- **🌍 CO₂ / appel** : 0.00000 g (France — 53 gCO₂/kWh)

### 💡 Suggestions d'amélioration

> **Score actuel : 18/123** — Score potentiel avec toutes les suggestions : **123/123** (+105 pts possibles)

🔴 Haute priorité : 4 | 🟡 Moyenne : 11 | ⚪ Basse : 3 | **Total : 18 suggestions**

#### 🔍 DE08 — Filtrage de champs (❌ Non validé — +15 pts possibles)

> Support a 'fields' parameter to reduce the payload. (0/2 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🔴 Haute | `GET /books` | Add a 'fields' query parameter for sparse fieldsets | +7.5 pts/endpoint (total gap: 15 pts) — lets clients request only needed fields, reducing payload |
| 🟡 Moyenne | `GET /books/{id}` | Add a 'fields' query parameter for sparse fieldsets | +7.5 pts/endpoint (total gap: 15 pts) — lets clients request only needed fields, reducing payload |

<details><summary>🔧 Comment implémenter</summary>

```
Spring Boot: Add an optional @RequestParam and filter the DTO:
  @GetMapping
  public ApiResponse<?> list(
      @RequestParam(required = false) String fields) {
    // If fields != null, use Jackson @JsonFilter or a projection
    // to return only the requested fields.
  }
Alternative: Use a custom Jackson MappingJacksonValue with a
SimpleFilterProvider that keeps only the requested properties.
OpenAPI: The 'fields' param will appear automatically.
```
</details>

#### 🗜️ DE01 — Compression Gzip (❌ Non validé — +15 pts possibles)

> The server must support Accept-Encoding: gzip. (0/2 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🔴 Haute | `ALL endpoints (server-level)` | Enable gzip compression on the server | +7.5 pts/endpoint (total gap: 15 pts) — typically 60-80% payload reduction |

<details><summary>🔧 Comment implémenter</summary>

```
Option 1 — Spring Boot application.yml:
  server:
    compression:
      enabled: true
      min-response-size: 1024
      mime-types: application/json,application/xml,text/html,text/plain

Option 2 — Nginx (if reverse proxy):
  gzip on;
  gzip_types application/json application/xml text/plain;
  gzip_min_length 1024;
  gzip_comp_level 6;

Both options apply to ALL endpoints automatically.
```
</details>

#### 💾 DE02/03 — Cache ETag/304 (❌ Non validé — +15 pts possibles)

> Individual resources must support ETag + If-None-Match -> 304. (0/1 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🔴 Haute | `GET /books/{id}` | Add ETag support and If-None-Match → 304 Not Modified | +15.0 pts/endpoint (total gap: 15 pts) — avoids resending unchanged resources, saves bandwidth |

<details><summary>🔧 Comment implémenter</summary>

```
Spring Boot: Use ShallowEtagHeaderFilter (zero-code) or manual ETags:

  Option A — Global filter (easiest):
  @Bean
  public FilterRegistrationBean<ShallowEtagHeaderFilter> etagFilter() {
    FilterRegistrationBean<ShallowEtagHeaderFilter> reg = new FilterRegistrationBean<>();
    reg.setFilter(new ShallowEtagHeaderFilter());
    reg.addUrlPatterns("/api/*");
    return reg;
  }

  Option B — Manual per endpoint:
  String etag = '"' + DigestUtils.md5DigestAsHex(body.getBytes()) + '"';
  if (request.checkNotModified(etag)) return null; // → 304
  return ResponseEntity.ok().eTag(etag).body(body);
```
</details>

#### 🔄 DE06 — Delta / Changes (❌ Non validé — +10 pts possibles)

> A /changes?since= endpoint or equivalent must exist. (0/2 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🟡 Moyenne | `GET /books/changes  (new endpoint)` | Add a delta/changes endpoint with a 'since' parameter | +5.0 pts/endpoint (total gap: 10 pts) — clients fetch only what changed since last sync |

<details><summary>🔧 Comment implémenter</summary>

```
Spring Boot: Add a new endpoint that filters by updatedAt:
  @GetMapping("/changes")
  public ApiResponse<List<T>> getChanges(
      @RequestParam @DateTimeFormat(iso = ISO.DATE_TIME) LocalDateTime since) {
    return ApiResponse.success(
        repository.findByUpdatedAtAfter(since));
  }

Prerequisite: Add an 'updatedAt' column with @UpdateTimestamp
to your entity, and a repository method findByUpdatedAtAfter().
Alternative: Add @RequestParam 'since' to existing /books.
```
</details>

#### ✂️ 206 — Range / Partial Content (❌ Non validé — +10 pts possibles)

> Support the Range header for large payloads. (0/2 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| ⚪ Basse | `GET /books/{id}` | Support HTTP Range header for partial content (206) | +10 pts — enables resumable downloads and partial fetches |
| ⚪ Basse | `GET /books` | Support HTTP Range header for partial content (206) | +10 pts — enables resumable downloads and partial fetches |

<details><summary>🔧 Comment implémenter</summary>

```
For JSON endpoints, Range/206 is rarely useful.
Focus on the file download endpoint(s) instead.
```
</details>

#### 📦 AR02 — Format binaire (CBOR) (❌ Non validé — +10 pts possibles)

> A binary-format endpoint (CBOR, protobuf...) must exist. (0/2 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| ⚪ Basse | `GET /books  (add CBOR variant)` | Add a binary format alternative (CBOR or Protobuf) | +10 pts — binary formats are 30-50% smaller than JSON |

<details><summary>🔧 Comment implémenter</summary>

```
Spring Boot + CBOR:
  1. Add dependency: com.fasterxml.jackson.dataformat:jackson-dataformat-cbor
  2. Register the converter:
     @Bean
     public HttpMessageConverter<Object> cborConverter(ObjectMapper mapper) {
       ObjectMapper cborMapper = new ObjectMapper(new CBORFactory());
       return new MappingJackson2CborHttpMessageConverter(cborMapper);
     }
  3. Clients send: Accept: application/cbor

Alternative (Protobuf):
  Add spring-boot-starter-protobuf and define .proto schemas.
  Register ProtobufHttpMessageConverter.
```
</details>

#### 📌 AR02_runtime_close (❌ Non validé — +7 pts possibles)

> Deploy the API as close as possible to consumers (CDN, edge, multi-region anycast). (0/2 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🟡 Moyenne | `AR02` | No cross-validated edge/CDN signal (runtime + HEAD). Place the API behind a multi-region edge/CDN (Cloudflare, CloudFront, Front Door, Fastly, Akamai…) to bring the runtime closer to consumers. | +7 pts (AR02). |
| 🟡 Moyenne | `AR02` | The OpenAPI spec declares only one server URL. Add multiple regional `servers[]` entries (e.g. eu-west, us-east) to document a multi-region deployment. | +7 pts (AR02). |
| 🟡 Moyenne | `AR02` | Enable HTTPS on the target to measure TLS latency and benefit from a modern edge/CDN. | +7 pts (AR02). |

#### 📌 AR01_event_driven (❌ Non validé — +6 pts possibles)

> Use an event-driven architecture (callbacks, webhooks, AsyncAPI, SSE, WebSocket, broker) to avoid polling. (0/2 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🟡 Moyenne | `AR01` | No EDA signal detected. Document your event flows with AsyncAPI or add callbacks/webhooks to your OpenAPI. | +6 pts (AR01). |

#### 👁️ LO01 — Observabilité (❌ Non validé — +5 pts possibles)

> Actuator / health / metrics must be exposed. (0/5 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🔴 Haute | `/actuator/health, /actuator/metrics` | Expose Spring Boot Actuator endpoints | +5 pts — essential for production monitoring |

<details><summary>🔧 Comment implémenter</summary>

```
Spring Boot application.yml:
  management:
    endpoints:
      web:
        exposure:
          include: health,info,metrics
    endpoint:
      health:
        show-details: when-authorized

Add dependency: spring-boot-starter-actuator (likely already present).
```
</details>

#### 🚦 US07 — Rate Limiting (❌ Non validé — +5 pts possibles)

> A rate-limiting mechanism must be present. (0/2 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🟡 Moyenne | `ALL endpoints (server-level)` | Add rate-limit response headers | +5 pts — protects the API from abuse and signals limits to clients |

<details><summary>🔧 Comment implémenter</summary>

```
Option 1 — Spring Boot filter:
  Add a HandlerInterceptor or OncePerRequestFilter that adds:
    X-RateLimit-Limit: 100
    X-RateLimit-Remaining: 97
    X-RateLimit-Reset: 1620000000

Option 2 — Use Bucket4j + Spring Boot Starter:
  <dependency>com.bucket4j:bucket4j-spring-boot-starter</dependency>
  Configure rate limits in application.yml per endpoint.

Option 3 — Nginx:
  limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
  location /api/ { limit_req zone=api burst=20; }
  add_header X-RateLimit-Limit 100;
```
</details>

#### 📌 AR04_scalable_infra (❌ Non validé — +5 pts possibles)

> Prefer auto-scalable infrastructure (HPA, KEDA, autoscaling, serverless). (0/2 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🟡 Moyenne | `AR04` | No auto-scaling signal detected in IaC/build files. | +5 pts (AR04). |
| 🟡 Moyenne | `AR04` | Enable HPA/KEDA (Kubernetes), Terraform/Bicep autoscaling, or deploy serverless (Azure Functions, AWS Lambda, Cloud Run). | +5 pts (AR04). |

#### 📌 AR05_cloud_footprint (❌ Non validé — +2 pts possibles)

> Track the carbon footprint through the cloud provider's native dashboard. (0/2 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🟡 Moyenne | `AR05` | No cloud provider detected through HTTP headers. If the API is hosted on AWS/Azure/GCP/OVH, check edge header exposure or manually confirm dashboard usage with ``--cloud-footprint-confirmed``. | +2 pts (AR05). |
| 🟡 Moyenne | `AR05` | No standard telemetry detected (/actuator/metrics, /metrics, /q/metrics). Expose metrics to feed the dashboard. | +2 pts (AR05). |


---

## 🌱 Creedengo Éco-Design : **88/100** — Grade **A** 🟢

> Analyse statique de l'éco-conception du code source via [Creedengo](https://github.com/green-code-initiative) / SonarQube

> ⚠️ **Seules les règles Creedengo/écodesign sont comptabilisées** dans le score et le récapitulatif ci-dessous. Les règles SonarQube générales sont listées séparément.

- **Langages détectés** : java
- **Principal** : java
- **Plugins Creedengo** : java

### 📊 Récapitulatif — Règles Creedengo écodesign uniquement

| Sévérité | Nombre |
|:--------:|-------:|
| 🔴 **Bloquant** | 0 |
| 🟠 **Critique** | 0 |
| 🟡 **Majeur** | 0 |
| ⚪ **Mineur** | 145 |
| 🔵 **Info** | 0 |
| **Total** | **145** |

- **Issues écodesign** : 145
- **Règles écodesign violées** : 2 / 17 analysées
- **Formule du score** : (1 − 2/17) × 100 = **88/100**
- **Effort de remédiation** : 12h35min

- **Lignes de code** : 1,017

### 🏷️ Catégories éco-design

| Catégorie | Issues | Règles |
|-----------|-------:|-------:|
| 🌱 Éco-conception générale | 143 | 1 |
| 💾 Utilisation mémoire | 2 | 1 |

### 📋 Règles Creedengo violées

| Sévérité | Règle | Issues | Catégorie |
|:--------:|-------|-------:|-----------|
| ⚪ MINOR | **GCI82** — Variable can be made constant | 143 | general |
| ⚪ MINOR | **GCI76** — Avoid usage of static collections. | 2 | memory |

### 📁 Fichiers les plus impactés (écodesign)

| Fichier | Issues |
|---------|-------:|
| `api/BookReactiveController.java` | 37 |
| `api/BookController.java` | 36 |
| `repo/BookRepository.java` | 19 |
| `observability/PayloadLoggingFilter.java` | 8 |
| `api/FieldSelector.java` | 7 |
| `web/GlobalExceptionHandler.java` | 7 |
| `domain/Book.java` | 6 |
| `repo/BookRepository.java` | 5 |
| `web/ApiError.java` | 5 |
| `web/RateLimitFilter.java` | 5 |
| *… et 6 autres* | |

---

### 🔧 Issues SonarQube générales (hors écodesign) — 16 issues

> Ces issues proviennent des règles SonarQube standard (qualité de code, bugs, sécurité). Elles ne sont **pas** comptabilisées dans le score Creedengo.

| Sévérité | Nombre |
|:--------:|-------:|
| 🟠 Critique | 3 |
| 🟡 Majeur | 7 |
| ⚪ Mineur | 5 |
| 🔵 Info | 1 |
| **Total** | **16** |

| Sévérité | Règle | Issues |
|:--------:|-------|-------:|
| 🟠 CRITICAL | **S1192** — S1192 | 3 |
| 🟡 MAJOR | **S6126** — S6126 | 5 |
| 🟡 MAJOR | **S108** — S108 | 1 |
| 🟡 MAJOR | **S107** — S107 | 1 |
| ⚪ MINOR | **S1170** — S1170 | 2 |
| ⚪ MINOR | **S1612** — S1612 | 1 |
| ⚪ MINOR | **S1602** — S1602 | 1 |
| ⚪ MINOR | **S1319** — S1319 | 1 |
| 🔵 INFO | **S1135** — S1135 | 1 |

- **Effort de remédiation SonarQube** : 1h26min

📅 *2026-05-01T10:02:38Z*

---

🌿 *API Green Score — [Framework](https://github.com/API-Green-Score/APIGreenScore) | [Training](https://github.com/API-Green-Score/training-student) | 🌱 [Creedengo](https://github.com/green-code-initiative) | Summit AXA 2026*

> 📊 Pour le dashboard interactif complet, ouvrez [`dashboard/index.html`](index.html)
