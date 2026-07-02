# 🌿 Green API Score Dashboard

> 📦 **Application : sample**
>
> **Devoxx France 2026 — Green Architecture : moins de gras, plus d'impact !**

📅 *Dernière analyse : 2026-07-02T10:00:00Z*

---

## 🟡 Green Score : **78/100** — Grade **B** 🥈

### 📋 Détail par règle

| Statut | Règle | Score | Max | Endpoints | Détail |
|:------:|-------|------:|----:|:---------:|--------|
| ✅ | DE11 Pagination | 15 | 15 | — | OK |
| ✅ | DE08 Filtrage champs | 15 | 15 | — |  |
| ✅ | DE01 Compression | 15 | 15 | — |  |
| ✅ | DE02/03 Cache ETag | 15 | 15 | — |  |
| ✅ | DE06 Delta | 10 | 10 | — |  |
| ❌ | 206 Range | 0 | 10 | — |  |
| ✅ | LO01 Observabilité | 5 | 5 | — |  |
| ⚠️ | US07 Rate Limit | 3 | 5 | — |  |
| ❌ | AR02 CBOR | 0 | 10 | — |  |


---

## 🏛️ Architecture : **19/23** 🟡

> **Ces règles pèsent 23 points** — au même titre que les règles code — mais sont souvent oubliées. Elles portent sur la topologie de l'API (événements, edge/CDN, dédup, autoscaling, empreinte cloud).

<svg xmlns="http://www.w3.org/2000/svg" width="260" height="260" viewBox="0 0 260 260"><polygon points="130.0,105.0 153.8,122.3 144.7,150.2 115.3,150.2 106.2,122.3" fill="none" stroke="#e5e7eb" stroke-width="1"/><polygon points="130.0,80.0 177.6,114.5 159.4,170.5 100.6,170.5 82.4,114.5" fill="none" stroke="#e5e7eb" stroke-width="1"/><polygon points="130.0,55.0 201.3,106.8 174.1,190.7 85.9,190.7 58.7,106.8" fill="none" stroke="#e5e7eb" stroke-width="1"/><polygon points="130.0,30.0 225.1,99.1 188.8,210.9 71.2,210.9 34.9,99.1" fill="none" stroke="#e5e7eb" stroke-width="1"/><line x1="130.0" y1="130.0" x2="130.0" y2="30.0" stroke="#d1d5db" stroke-width="1"/><line x1="130.0" y1="130.0" x2="225.1" y2="99.1" stroke="#d1d5db" stroke-width="1"/><line x1="130.0" y1="130.0" x2="188.8" y2="210.9" stroke="#d1d5db" stroke-width="1"/><line x1="130.0" y1="130.0" x2="71.2" y2="210.9" stroke="#d1d5db" stroke-width="1"/><line x1="130.0" y1="130.0" x2="34.9" y2="99.1" stroke="#d1d5db" stroke-width="1"/><polygon points="130.0,30.0 197.9,107.9 188.8,210.9 71.2,210.9 130.0,130.0" fill="rgba(34,197,94,0.35)" stroke="#16a34a" stroke-width="2"/><text x="130.0" y="15.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="#374151">AR01 (6/6)</text><text x="239.4" y="94.5" text-anchor="start" font-size="11" font-family="sans-serif" fill="#374151">AR02 (5/7)</text><text x="197.6" y="223.0" text-anchor="start" font-size="11" font-family="sans-serif" fill="#374151">AR03 (3/3)</text><text x="62.4" y="223.0" text-anchor="end" font-size="11" font-family="sans-serif" fill="#374151">AR04 (5/5)</text><text x="20.6" y="94.5" text-anchor="end" font-size="11" font-family="sans-serif" fill="#374151">AR05 (0/2)</text></svg>

| Statut | Règle | Score | Max | Signaux détectés |
|:------:|-------|------:|----:|------------------|
| ✅ | **AR01** Event-Driven Architecture | 6 | 6 | asyncapi, runtime+spec |
| ⚠️ | **AR02** Runtime proche du consommateur | 5 | 7 | cdn_header, tls_handshake_latency |
| ✅ | **AR03** Une seule API par besoin | 3 | 3 | — |
| ✅ | **AR04** Infrastructure scalable | 5 | 5 | — |
| ❌ | **AR05** Cloud footprint dashboard | 0 | 2 | — |


---

## 📜 ADR compliance : **6/8** (75.0%) 🟡

> Total ADR : **10** — Acceptés : **8** — Passés : **6** — Échecs : **2** — Ignorés (deprecated/proposed) : **2**

| Statut | ADR | Titre | Règles | Checks passés |
|:------:|:---:|-------|--------|:--------------|
| ✅ | `0001` | Adopt Green API Score | — | 0/0 |
| ✅ | `0002` | Pagination | DE11 | 1/1 |
| ❌ | `0009` | Auto-scaling AR04 | AR04 | 0/1 |

### ❌ ADR en échec — détail

#### `0009` — Auto-scaling AR04

- ❌ **iac_signal** — Aucun signal parmi hpa,keda,…


### 📊 Mesures (legacy)

| Mesure | Taille | Temps | HTTP |
|--------|-------:|------:|-----:|

### 🔑 Métriques clés

- **Endpoints mesurés** : 0
- **Transfert total** : 0 B
- **Temps moyen** : 0.000s
- **⚡ Énergie totale / appel** : 0.0000 Wh
- **🌍 CO₂ / appel** : 0.00000 g (France — 53 gCO₂/kWh)

### 💡 Suggestions d'amélioration

> ✅ **Aucune suggestion d'amélioration** — Score actuel : **78/100** — toutes les règles analysées sont conformes.

---

🌿 *API Green Score — [Framework](https://github.com/API-Green-Score/APIGreenScore) | [Training](https://github.com/API-Green-Score/training-student) | 🌱 [Creedengo](https://github.com/green-code-initiative) | Devoxx France 2026*

> 📊 Pour le dashboard interactif complet, ouvrez [`dashboard/index.html`](index.html)
