# 🌿 Green API Score Dashboard

> 📦 **Application : APIXP Orchestrateur FrontDeGestion**
>
> **Devoxx France 2026 — Green Architecture : moins de gras, plus d'impact !**

📅 *Dernière analyse : 2026-10-08T16:11:55Z*

---

## 🔴 Green Score : **9/100** — Grade **E** 📉

### 📋 Détail par règle

| Statut | Règle | Score | Max | Endpoints | Détail |
|:------:|-------|------:|----:|:---------:|--------|
| ❌ | DE11 Pagination | 0 | 15 | 0/1 | No pagination on collection endpoints |
| ❌ | DE08 Filtrage champs | 0 | 15 | 0/3 | No field filter found |
| ❌ | DE01 Compression | 0 | 15 | 0/4 | Neither gzip nor brotli detected |
| ❌ | DE02/03 Cache ETag | 0 | 15 | 0/2 | ETag/304 not detected |
| ❌ | DE06 Delta | 0 | 10 | 0/3 | No delta endpoint found |
| ❌ | 206 Range | 0 | 10 | 0/3 | Range not supported |
| ⚠️ | LO01 Observabilité | 4 | 5 | 4/5 | Actuator/health detected |
| ❌ | US07 Rate Limit | 0 | 5 | 0/4 | Assumed present (API running, no explicit headers) |
| ❌ | AR02 CBOR | 0 | 10 | 0/4 | No binary format endpoint (spec + runtime probes empty) |


---

## 🏛️ Architecture : **5/23** 🔴

> **Ces règles pèsent 23 points** — au même titre que les règles code — mais sont souvent oubliées. Elles portent sur la topologie de l'API (événements, edge/CDN, dédup, autoscaling, empreinte cloud).

<svg xmlns="http://www.w3.org/2000/svg" width="260" height="260" viewBox="0 0 260 260"><polygon points="130.0,105.0 153.8,122.3 144.7,150.2 115.3,150.2 106.2,122.3" fill="none" stroke="#e5e7eb" stroke-width="1"/><polygon points="130.0,80.0 177.6,114.5 159.4,170.5 100.6,170.5 82.4,114.5" fill="none" stroke="#e5e7eb" stroke-width="1"/><polygon points="130.0,55.0 201.3,106.8 174.1,190.7 85.9,190.7 58.7,106.8" fill="none" stroke="#e5e7eb" stroke-width="1"/><polygon points="130.0,30.0 225.1,99.1 188.8,210.9 71.2,210.9 34.9,99.1" fill="none" stroke="#e5e7eb" stroke-width="1"/><line x1="130.0" y1="130.0" x2="130.0" y2="30.0" stroke="#d1d5db" stroke-width="1"/><line x1="130.0" y1="130.0" x2="225.1" y2="99.1" stroke="#d1d5db" stroke-width="1"/><line x1="130.0" y1="130.0" x2="188.8" y2="210.9" stroke="#d1d5db" stroke-width="1"/><line x1="130.0" y1="130.0" x2="71.2" y2="210.9" stroke="#d1d5db" stroke-width="1"/><line x1="130.0" y1="130.0" x2="34.9" y2="99.1" stroke="#d1d5db" stroke-width="1"/><polygon points="130.0,130.0 130.0,130.0 188.8,210.9 130.0,130.0 34.9,99.1" fill="rgba(34,197,94,0.35)" stroke="#16a34a" stroke-width="2"/><text x="130.0" y="15.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="#374151">AR01 (0/6)</text><text x="239.4" y="94.5" text-anchor="start" font-size="11" font-family="sans-serif" fill="#374151">AR02 (0/7)</text><text x="197.6" y="223.0" text-anchor="start" font-size="11" font-family="sans-serif" fill="#374151">AR03 (3/3)</text><text x="62.4" y="223.0" text-anchor="end" font-size="11" font-family="sans-serif" fill="#374151">AR04 (0/5)</text><text x="20.6" y="94.5" text-anchor="end" font-size="11" font-family="sans-serif" fill="#374151">AR05 (2/2)</text></svg>

| Statut | Règle | Score | Max | Signaux détectés |
|:------:|-------|------:|----:|------------------|
| ❌ | **AR01** Event-Driven Architecture | 0 | 6 | — |
| ❌ | **AR02** Runtime proche du consommateur | 0 | 7 | tls_skip |
| ✅ | **AR03** Une seule API par besoin | 3 | 3 | info |
| ❌ | **AR04** Infrastructure scalable | 0 | 5 | — |
| ✅ | **AR05** Cloud footprint dashboard | 2 | 2 | attestation, observability |


---

## 📜 ADR compliance : **2/10** (20.0%) 🔴

> Total ADR : **10** — Acceptés : **10** — Passés : **2** — Échecs : **8** — Ignorés (deprecated/proposed) : **0**

| Statut | ADR | Titre | Règles | Checks passés |
|:------:|:---:|-------|--------|:--------------|
| ✅ | `1` | Adopt the API Green Score framework | — | 0/0 |
| ❌ | `2` | Mandatory pagination on collection endpoints (DE11) | DE11 | 0/2 |
| ❌ | `3` | ETag caching strategy on GET single-resource (DE02/DE03) | DE02, DE03 | 0/2 |
| ❌ | `4` | Enable GZIP compression middleware (DE01) | DE01 | 0/1 |
| ❌ | `5` | Field-filtering via ?fields query param (DE08) | DE08 | 0/1 |
| ❌ | `6` | Expose /health and /metrics observability endpoints (LO01) | LO01, AR05 | 0/1 |
| ❌ | `7` | Prefer events (SSE / AsyncAPI) over polling (AR01) | AR01, DE06 | 1/2 |
| ❌ | `8` | Deploy runtime in ≥ 2 regions close to consumers (AR02) | AR02 | 0/2 |
| ❌ | `9` | Auto-scaling and serverless where applicable (AR04) | AR04 | 0/1 |
| ✅ | `10` | ADR gate — every architecture decision is verified in CI | — | 0/0 |

### ❌ ADR en échec — détail

#### `2` — Mandatory pagination on collection endpoints (DE11)

- ❌ **has_pagination_params** — 2 endpoint(s) sans page+size
- ❌ **has_pagination_params** — 2 endpoint(s) sans limit|offset

#### `3` — ETag caching strategy on GET single-resource (DE02/DE03)

- ❌ **response_header_present** — En-tête `etag` jamais observé
- ❌ **endpoint_returns_status** — Aucun endpoint sur /** ne déclare 304

#### `4` — Enable GZIP compression middleware (DE01)

- ❌ **response_header_present** — En-tête `content-encoding` jamais observé

#### `5` — Field-filtering via ?fields query param (DE08)

- ❌ **has_pagination_params** — 2 endpoint(s) sans fields

#### `6` — Expose /health and /metrics observability endpoints (LO01)

- ❌ **has_health_endpoint** — Aucun endpoint santé parmi ['/health', '/actuator/health', '/metrics', '/actuator/prometheus', '/q/metrics']

#### `7` — Prefer events (SSE / AsyncAPI) over polling (AR01)

- ❌ **sse_endpoint** — Aucun endpoint SSE déclaré sur /**/events

#### `8` — Deploy runtime in ≥ 2 regions close to consumers (AR02)

- ❌ **openapi_field** — servers count=1 (attendu >= 2)
- ❌ **cdn_header_present** — Aucun des en-têtes CDN ['cf-ray', 'x-amz-cf-id', 'x-azure-ref', 'x-served-by', 'x-akamai-request-id'] observé

#### `9` — Auto-scaling and serverless where applicable (AR04)

- ❌ **iac_signal** — Aucun signal parmi ['hpa', 'keda', 'terraform-autoscale', 'bicep-autoscale', 'serverless-config', 'faas-deps'] (scanné: ∅)


### 📊 Mesures par endpoint (API découverte)

| Méthode | Endpoint | Taille | Temps | HTTP |
|:-------:|----------|-------:|------:|-----:|
| GET | `/agreements/{identifier}/operations` | 138 B | 0.012s | 400 |
| POST | `/agreements/{identifier}/operations` | 138 B | 0.003s | 400 |
| GET | `/swagger` | 18.9 KB | 0.003s | 200 |
| GET | `/agreements/{identifier}` | 127 B | 0.009s | 400 |

### 🔑 Métriques clés

- **Endpoints mesurés** : 4
- **Transfert total** : 19.3 KB
- **Transfert moyen / endpoint** : 4.8 KB
- **Temps moyen** : 0.007s
- **⚡ Énergie totale / appel** : 0.0013 Wh
- **🌍 CO₂ / appel** : 0.00007 g (France — 53 gCO₂/kWh)

### 💡 Suggestions d'amélioration

> **Score actuel : 9/123** — Score potentiel avec toutes les suggestions : **123/123** (+114 pts possibles)

🔴 Haute priorité : 7 | 🟡 Moyenne : 10 | ⚪ Basse : 3 | **Total : 20 suggestions**

#### 📄 DE11 — Pagination (❌ Non validé — +15 pts possibles)

> Les endpoints de collection doivent supporter la pagination (page/size ou limit/offset). (0/1 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🔴 Haute | `GET /swagger` | Add pagination parameters (page & size) | +15.0 pts/endpoint (total gap: 15 pts) — reduces payload size for large collections |

<details><summary>🔧 Comment implémenter</summary>

```
Spring Boot: Change return type from List<T> to Page<T> and add @RequestParam defaultValue parameters:
  @GetMapping
  public ApiResponse<Page<T>> list(
      @RequestParam(defaultValue = "0") int page,
      @RequestParam(defaultValue = "20") int size) {
    return ApiResponse.success(repository.findAll(PageRequest.of(page, size)));
  }
OpenAPI: params 'page' and 'size' will appear automatically via springdoc.
```
</details>

#### 🔍 DE08 — Filtrage de champs (❌ Non validé — +15 pts possibles)

> Supporter un parametre 'fields' pour reduire le payload. (0/3 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🟡 Moyenne | `GET /agreements/{identifier}/operations` | Add a 'fields' query parameter for sparse fieldsets | +5.0 pts/endpoint (total gap: 15 pts) — lets clients request only needed fields, reducing payload |
| 🔴 Haute | `GET /swagger` | Add a 'fields' query parameter for sparse fieldsets | +5.0 pts/endpoint (total gap: 15 pts) — lets clients request only needed fields, reducing payload |
| 🟡 Moyenne | `GET /agreements/{identifier}` | Add a 'fields' query parameter for sparse fieldsets | +5.0 pts/endpoint (total gap: 15 pts) — lets clients request only needed fields, reducing payload |

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

> Le serveur doit supporter Accept-Encoding: gzip. (0/4 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🔴 Haute | `ALL endpoints (server-level)` | Enable gzip compression on the server | +3.8 pts/endpoint (total gap: 15 pts) — typically 60-80% payload reduction |

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

> Les ressources unitaires doivent supporter ETag + If-None-Match -> 304. (0/2 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🔴 Haute | `GET /agreements/{identifier}/operations` | Add ETag support and If-None-Match → 304 Not Modified | +7.5 pts/endpoint (total gap: 15 pts) — avoids resending unchanged resources, saves bandwidth |
| 🔴 Haute | `GET /agreements/{identifier}` | Add ETag support and If-None-Match → 304 Not Modified | +7.5 pts/endpoint (total gap: 15 pts) — avoids resending unchanged resources, saves bandwidth |

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

> Un endpoint /changes?since= ou equivalent doit exister. (0/3 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🟡 Moyenne | `GET /swagger/changes  (new endpoint)` | Add a delta/changes endpoint with a 'since' parameter | +3.3 pts/endpoint (total gap: 10 pts) — clients fetch only what changed since last sync |

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
Alternative: Add @RequestParam 'since' to existing /swagger.
```
</details>

#### ✂️ 206 — Range / Partial Content (❌ Non validé — +10 pts possibles)

> Supporter le header Range pour les gros payloads. (0/3 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| ⚪ Basse | `GET /agreements/{identifier}/operations` | Support HTTP Range header for partial content (206) | +10 pts — enables resumable downloads and partial fetches |
| ⚪ Basse | `GET /agreements/{identifier}` | Support HTTP Range header for partial content (206) | +10 pts — enables resumable downloads and partial fetches |

<details><summary>🔧 Comment implémenter</summary>

```
For JSON endpoints, Range/206 is rarely useful.
Focus on the file download endpoint(s) instead.
```
</details>

#### 📦 AR02 — Format binaire (CBOR) (❌ Non validé — +10 pts possibles)

> Un endpoint en format binaire (CBOR, protobuf...) doit exister. (0/4 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| ⚪ Basse | `GET /swagger  (add CBOR variant)` | Add a binary format alternative (CBOR or Protobuf) | +10 pts — binary formats are 30-50% smaller than JSON |

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

> Déployer l'API au plus près des consommateurs (CDN, edge, anycast multi-régions). (0/4 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🟡 Moyenne | `AR02` | Aucun signal d'edge/CDN cross-validé (runtime + HEAD). Mettre l'API derrière un edge/CDN multi-régions (Cloudflare, CloudFront, Front Door, Fastly, Akamai…) pour rapprocher le runtime des consommateurs. | +7 pts (AR02). |
| 🟡 Moyenne | `AR02` | La spec OpenAPI ne déclare qu'une seule URL de serveur. Ajouter plusieurs entrées `servers[]` régionales (ex: eu-west, us-east) pour documenter un déploiement multi-régions. | +7 pts (AR02). |
| 🟡 Moyenne | `AR02` | Activer HTTPS sur la cible pour permettre la mesure de latence TLS et bénéficier d'un edge/CDN moderne. | +7 pts (AR02). |

#### 📌 AR01_event_driven (❌ Non validé — +6 pts possibles)

> Utiliser une architecture événementielle (callbacks, webhooks, AsyncAPI, SSE, WebSocket, broker) pour éviter le polling. (0/4 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🔴 Haute | `POST /agreements/{identifier}/operations` | Publier un événement domaine après mutation (Kafka/RabbitMQ/Azure Service Bus/EventBridge) pour découpler les consommateurs. Documenter via callbacks (OAS 3.x) ou un AsyncAPI dédié. | +6 pts (AR01) — supprime un cycle de polling, réduit la bande passante et la charge serveur. |
| 🟡 Moyenne | `AR01` | Aucun signal EDA détecté mais 1 opportunité(s) de migration vers SSE/AsyncAPI/WebSocket trouvées (cf. EDA Advisor). | +6 pts (AR01). |

<details><summary>🔧 Comment implémenter</summary>

```
Condition détectée: mutating-without-callback
Indice: Mutation declared but no OAS callbacks/webhooks
Cible recommandée: Domain Event publication
```
</details>

#### 🚦 US07 — Rate Limiting (❌ Non validé — +5 pts possibles)

> Un mecanisme de rate limiting doit etre present. (0/4 endpoints validés)

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

> Préférer une infrastructure auto-scalable (HPA, KEDA, autoscale, serverless). (0/4 endpoints validés)

| Priorité | Cible | Action | Impact |
|:--------:|-------|--------|--------|
| 🟡 Moyenne | `AR04` | Aucun signal d'auto-scaling détecté dans les fichiers IaC/build. | +5 pts (AR04). |
| 🟡 Moyenne | `AR04` | Activer HPA/KEDA (Kubernetes), autoscale Terraform/Bicep, ou déployer en serverless (Azure Functions, AWS Lambda, Cloud Run). | +5 pts (AR04). |

#### 👁️ LO01 — Observabilité (⚠️ Partiel (4/5) — +1 pts possibles)

> Actuator / health / metrics doit etre expose. (4/5 endpoints validés)

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
| ⚪ **Mineur** | 162 |
| 🔵 **Info** | 0 |
| **Total** | **162** |

- **Issues écodesign** : 162
- **Règles écodesign violées** : 2 / 17 analysées
- **Formule du score** : (1 − 2/17) × 100 = **88/100**
- **Effort de remédiation** : 13h45min

- **Lignes de code** : 4,553

### 🏷️ Catégories éco-design

| Catégorie | Issues | Règles |
|-----------|-------:|-------:|
| 🌱 Éco-conception générale | 161 | 1 |
| 💾 Utilisation mémoire | 1 | 1 |

### 📋 Règles Creedengo violées

| Sévérité | Règle | Issues | Catégorie |
|:--------:|-------|-------:|-----------|
| ⚪ MINOR | **GCI82** — Variable can be made constant | 161 | general |
| ⚪ MINOR | **GCI76** — Avoid usage of static collections. | 1 | memory |

### 📁 Fichiers les plus impactés (écodesign)

| Fichier | Issues |
|---------|-------:|
| `controller/AgreementManagementController.java` | 27 |
| `mapper/EffectiveDateTimeModelMapper.java` | 27 |
| `services/ValidatorService.java` | 22 |
| `mapper/EligibilityRequestMapper.java` | 12 |
| `error/ProblemDetailFactory.java` | 11 |
| `services/OrchIardPartEligibilityService.java` | 9 |
| `mapper/ActionDeterminationMapper.java` | 8 |
| `services/ContratsIardService.java` | 6 |
| `error/ApiCallException.java` | 5 |
| `error/AuthorizationControlException.java` | 5 |
| *… et 10 autres* | |

---

### 🔧 Issues SonarQube générales (hors écodesign) — 12 issues

> Ces issues proviennent des règles SonarQube standard (qualité de code, bugs, sécurité). Elles ne sont **pas** comptabilisées dans le score Creedengo.

| Sévérité | Nombre |
|:--------:|-------:|
| 🟡 Majeur | 6 |
| ⚪ Mineur | 1 |
| 🔵 Info | 5 |
| **Total** | **12** |

| Sévérité | Règle | Issues |
|:--------:|-------|-------:|
| 🟡 MAJOR | **S125** — S125 | 5 |
| 🟡 MAJOR | **S1854** — S1854 | 1 |
| ⚪ MINOR | **S1481** — S1481 | 1 |
| 🔵 INFO | **S2143** — S2143 | 3 |
| 🔵 INFO | **S1135** — S1135 | 1 |
| 🔵 INFO | **S8688** — S8688 | 1 |

- **Effort de remédiation SonarQube** : 1h21min

📅 *2026-10-08T16:14:36Z*

---

🌿 *API Green Score — [Framework](https://github.com/API-Green-Score/APIGreenScore) | [Training](https://github.com/API-Green-Score/training-student) | 🌱 [Creedengo](https://github.com/green-code-initiative) | Devoxx France 2026*

> 📊 Pour le dashboard interactif complet, ouvrez [`dashboard/index.html`](index.html)
