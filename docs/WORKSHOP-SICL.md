# Atelier API Green Score Analyzer — Journée dév SICL

> Format : **1h30**, hands-on, par **binôme ou trinôme**.
> Chaque équipe travaille sur **une API qui tourne en local** sur sa machine.

---

## Objectif de l'atelier

À la fin de l'atelier, chaque équipe doit avoir un dashboard avec mes résultats de l'API Green Score et Creedengo pour son projet.

---

## Organisation

| Élément | Détail |
|---------|--------|
| Équipes | 2 à 3 personnes. |
| Application | Une API Java du SICL. À défaut : un sample dans [`samples/`](../samples/). |

### Déroulé

| Bloc | Livrable |
|------|----------|
| Étape 1 — Lancer son API en local | API répond sur `localhost`, Swagger accessible |
| Étape 2 — Installer l'analyzer | Analyzer installé et premier test exécuté |
| Étape 3 — Analyse baseline Green API | Dashboard, rapport initial et score notés |
| Étape 4 — Analyse Creedengo | Score Creedengo et règles les plus violées relevés |
| Étape 5 — Restitution | Retour sur l'atelier |
| Partie 2 (bonus) — Pipeline CI | Pipeline exécutée sur la PR |

---

## Prérequis (à vérifier avant l'atelier)

| Outil | Vérification | Remarque |
|-------|--------------|----------|
| JDK 17+ | `java -version` | |
| Python 3.10+ | `python --version` | |
| Bash | `bash --version` | Sous Windows : **Git Bash** ou **WSL** (pas PowerShell). |
| Git, curl | `git --version` / `curl --version` | |
| Podman | `podman --version` | **Uniquement** pour Creedengo (SonarQube). |

Cloner le dépôt, changer de branche (feat/atelier-journee-dev) et installer les dépendances Python :

```bash
git clone https://axafrance@dev.azure.com/axafrance/GreenIT/_git/axa-apigreenscoreanalyzer
pip install -r scripts/requirements.txt
```
---

## Étape 1 — Lancer son API Java en local

### 1.1 Choisir l'application

- **Option A (recommandée)** : l'API Java de l'équipe.
- **Option B (secours)** : le sample fourni.

```bash
cd samples/java-spring
mvn spring-boot:run
```

### 1.2 Vérifier que l'API répond

Adapter le port si nécessaire (par défaut `8080`).

```bash
http://localhost:8080/actuator/health
http://localhost:8080/v3/api-docs
```

### 1.3 Checklist de l'étape

- [ ] L'application démarre sans erreur.
- [ ] Une URL de santé répond en `200`.
- [ ] Le contrat OpenAPI est accessible (`/v3/api-docs` ou `/swagger`) en `200`.
- [ ] Les endpoints de collection retournent des données (base locale / données de test).
- [ ] Si l'API est protégée : un **Bearer token** de test est disponible (ne **jamais** le committer).


### Dépannage rapide

| Symptôme | Piste |
|----------|-------|
| Port 8080 occupé | Changer `server.port` ou arrêter l'autre processus. |
| 401/403 sur Swagger | Ouvrir le chemin Swagger dans la config de sécurité en profil local, ou fournir `--bearer`. |
| `/v3/api-docs` absent | Ajouter la dépendance `springdoc-openapi-starter-webmvc-ui`. |
| Base de données requise | Utiliser un profil `local` avec base H2 en mémoire. |

---

## Étape 2 — Installer l'analyzer

Depuis la racine du dépôt de l'analyzer :

```bash
bash scripts/start.sh --help
```

Si l'API est **déjà démarrée** (étape 1), un premier test à vide :

```bash
bash scripts/start.sh --target http://localhost:8080
```

- [ ] Le script détecte l'API et termine sans erreur.
- [ ] `reports/latest-report.json` est créé.
- [ ] `dashboard/index.html` s'ouvre.

---

## Étape 3 — Analyse baseline Green API

### 3.1 Lancer l'analyse

**Cas 1 : l'API tourne déjà**

```bash
bash scripts/start.sh \
  --target http://localhost:8080 \
  --swagger http://localhost:8080/v3/api-docs \
  --source-dir ./chemin/vers/mon-app \
  --appname nom-du-projet
```

**Cas 2 : laisser l'analyzer compiler et démarrer l'API**

```bash
bash scripts/start.sh \
  --stack java \
  --build-and-run \
  --source-dir ./chemin/vers/mon-app \
  --appname nom-du-projet
```

**Cas 3 : API protégée**

```bash
BEARER_TOKEN="<token-de-test>" bash scripts/start.sh --target http://localhost:8080
```

> Les chemins avec espaces doivent être entre guillemets.
> `--debug` active les traces de diagnostic.

### 3.2 Lire le dashboard

Ouvrir `dashboard/index.html` et relever :

| Information | Score |
|-------------|--------------------|
| API Green Score (/100) | |
| Grade (A+ … E) | |
| Score architecture (/23) | |
| Règles en échec (liste) | |
| Endpoint le plus coûteux (taille / temps) | |

### 3.3 Rappel des règles

| Thème | Règles |
|-------|--------|
| Performance | Pagination (DE11), Filtrage `fields` (DE08), Compression gzip (DE01) |
| Cache | ETag / 304 (DE02/DE03), Delta `/changes` (DE06) |
| Scalabilité | Range / 206, Format binaire (BIN01) |
| Observabilité / Protection | Health / Metrics (LO01), Rate limiting (US07) |
| Architecture | Event-driven (AR01), Proximité runtime (AR02), API unique (AR03), Scalabilité infra (AR04), Empreinte cloud (AR05) |

**Discussion en équipe** : quelles règles sont en échec, et lesquelles sont les plus simples à corriger ?

---

## Étape 4 — Analyse Creedengo

Creedengo analyse le **code source** (anti-patterns d'éco-conception) via SonarQube.
Il nécessite Podman ou Docker.

```bash
bash scripts/start.sh \
  --stack java \
  --source-dir ./chemin/vers/mon-app \
  --target http://localhost:8080 \
  --creedengo
```

Ou seul :

```bash
bash scripts/creedengo-analyzer.sh
```

Relever dans le dashboard :

| Information | Score |
|-------------|--------------------|
| Score Creedengo (/100) | |
| Grade | |
| Règles les plus violées (GCI…) | |

Règles Java fréquentes : `GCI1` / `GCI72` (requêtes en boucle), `GCI74` (`SELECT *`), `GCI77` (`Pattern.compile`), `GCI79` (try-with-resources), `GCI82` (variables `final`), `GCI94` (`orElseGet`).

> L'API Green Score (API en fonctionnement) et le score Creedengo (code source) sont **distincts**.

---

## Étape 5 — Restitution

Chaque équipe complète et partage :

| Indicateur | Score |
|------------|-------|
| API Green Score | |
| Grade | |
| Score Creedengo | |
| Règles corrigées | |
| Difficulté rencontrée | |
| Recommendations | |

Le rapport précédent sert de baseline : le dashboard affiche l'évolution.

Si vous avez encore du temps, n'hésitez pas à fixer dans votre code une ou 2 règles et faire un comparatif avant / après

---

## Partie 2 — Pour les plus rapides : pipeline CI (bonus)

Intégrer l'analyzer dans la pipeline du projet (Azure DevOps ou GitHub Actions). Modèles : [`templates/ci`](../templates/ci) et [CI-INTEGRATION.md](CI-INTEGRATION.md).

La pipeline (`pr-green-api-axa.yml`) :

- se déclenche sur **PR** et **hebdomadairement** (dimanche) ;
- installe JDK 17, Maven et Python ;
- clone l'analyzer ;
- exécute `scripts/start.sh` avec les paramètres ;
- analyse Creedengo, Green Score et OpenAPI.

### Recommandations

| Sujet | À vérifier |
|-------|-----------|
| Variables | `TARGETS`, `SWAGGER_URL`, `STACK`, `BUILD_AND_RUN` renseignées. |
| Swagger accessible | Depuis l'agent CI : authentification et réponse `200` sur `/swagger` ou `/v3/api-docs`. |
| Modules | Noms des modules Maven/Gradle corrects ; bon sous-répertoire ciblé (`JAVA_MODULE`). |
| Secrets | `API_TOKEN`, `CLIENT_SECRET`, etc. dans les variables **secrètes** de la CI, jamais dans le YAML ni les logs. |

- [ ] Pipeline ajoutée dans une branche.
- [ ] Première exécution réussie.
- [ ] Rapport / dashboard publié en artefact.

---

## Dépannage général

| Problème | Solution |
|----------|----------|
| `start.sh` ne se lance pas sous Windows | Utiliser Git Bash ou WSL. |
| Aucun endpoint découvert | Fournir `--swagger <url>` explicitement ; vérifier le `200` sur le contrat OpenAPI. |
| Score très bas sur tout | L'API renvoie peut-être des erreurs (401/500) : vérifier les codes HTTP dans le rapport. |
| Creedengo échoue | Vérifier que Podman/Docker tourne ; port SonarQube `9100` libre (`SONAR_PORT`). |
| Build Java échoue (Lombok…) | `LOMBOK_VERSION=<version>` ; en multi-module, `JAVA_MODULE=<module>`. |
| Plus de détails | Relancer avec `--debug`. |

---

## Ressources

- [README du projet](../README.md) · [HOWTO](HOWTO.md) · [Intégration CI](CI-INTEGRATION.md)
- `dashboard/` — résultats générés
- Grille **API GreenScore v1.2** (PDF) — voir la slide « Ressources recommandées »
- Sobri-IT — AXA France Green Champions
