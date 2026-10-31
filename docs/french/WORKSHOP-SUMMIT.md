# Atelier API Green Score Analyzer — Summit

> Format : **1 heure**, avec des exercices pratiques, à réaliser **seul ou en binôme**.
> L'atelier propose trois parcours : explorer le dashboard, avoir un score de l'API Green Score sans API en cours d'exécution ou analyser une application
> déjà accessible.

---

## Objectif de l'atelier

Découvrir le dashboard de l'API Green Score et, selon les ressources dont vous
disposez, générer un rapport à partir d'une spécification OpenAPI ou d'une API
en cours d'exécution. **Aucune application Java, .NET ou Python n'est nécessaire**
pour réaliser les parties 1 et 2.

---

## Prérequis

| Outil | Requis | Vérification | Remarque |
|-------|--------|--------------|----------|
| Navigateur Web | ✅ | — | Aucun outil de développement requis. |
| Git Bash | ✅ | `bash --version` | **Obligatoire** pour exécuter les scripts de l'atelier. N'utilisez pas PowerShell, l'invite de commandes ou WSL. |
| Python 3.10+ | ✅ | `python --version` ou `python3 --version` | Nécessaire pour exécuter tous les scripts : [Installation Windows](https://www.python.org/ftp/python/pymanager/python-manager-26.4.msix), [Installation macOS](https://www.python.org/ftp/python/3.15.2/python-3.15.2-macos11.pkg) |
| Docker ou Podman | ❌ | — | Facultatif : requis uniquement pour la partie 4 (Creedengo), qui démarre SonarQube dans un conteneur. |
| Java | ❌ | — | Facultatif : vous pouvez utiliser une application existante. |
| .NET | ❌ | — | Facultatif : vous pouvez utiliser une application existante. |

Docker ou Podman n'est pas nécessaire pour les parties 1 à 3. La partie 4 est
facultative et analyse le code source ; elle ne nécessite pas que l'API soit
démarrée.

Clonez le dépôt et installez les dépendances de l'analyzer depuis **Git Bash** :

```bash
git clone https://github.com/thiernodialloAFA/axa-apigreenscoreanalyzer.git
cd axa-apigreenscoreanalyzer
python -m pip install -r scripts/requirements.txt
```

---

## Partie 1 — Explorer le tableau de bord existant

Cette partie est ouverte à toutes et à tous, y compris aux personnes qui ne
développent pas d'API et qui ne disposent pas d'une application Java, .NET ou
Python.

1. Ouvrez le dossier du dépôt de l'analyzer dans l'Explorateur de fichiers.
2. Ouvrez le fichier [dashboard/index.html](../../dashboard/index.html) dans votre navigateur Web (par exemple, en double-cliquant sur le fichier ou en choisissant **Ouvrir avec** puis votre navigateur).
3. Explorez le dashboard de l'API Green Score et ses différentes sections. Le dashboard affiche un rapport complet que vous pouvez générer dans les parties 2 ou 3.

Aucun terminal, aucune API ni aucun langage de programmation n'est nécessaire
pour cette partie.

---

## Partie 2 — Générer un score uniquement à partir d'une spécification Swagger/OpenAPI

Cette partie ne nécessite **ni API en cours d'exécution ni application dans un
langage particulier**. Elle utilise le mode `swagger-only` : l'analyzer lit un fichier swagger (JSON ou YAML) et n'envoie aucune requête aux points de terminaison de
l'API.

> **Git Bash est obligatoire** pour cette partie. Exécutez les commandes
> ci-dessous dans Git Bash, depuis la racine du dépôt cloné, et non dans
> PowerShell, l'invite de commandes ou WSL. Vous pouvez aussi installer le plugin `Start git-bash` dans VS Code.

### 2.1 Choisir un swagger

Utilisez le swagger d'exemple de l'atelier, créez un nouveau swagger ou importez le swagger d'une de vos applications
existantes. Le swwagger doit respecter les normes OpenAPI prises en charge
et être disponible au format JSON/YAML. Une application en cours
d'exécution n'est pas nécessaire pour cette partie.

Voici la commande pour lancer la commande avec le [swagger présent](../../dashboard/sample-swagger.yaml) dans le projet : 

```bash
bash scripts/start.sh --swagger dashboard/sample-swagger.yaml --appname workshop-swagger-only
```

Si le est disponible à une URL, remplacez le chemin de
l'exemple, par exemple :

```bash
bash scripts/start.sh --swagger "https://petstore3.swagger.io/api/v3/openapi.json" --appname petstore-swagger
```

N'ajoutez **pas** `--target` : son omission active le mode `swagger-only` et
garantit que l'analyzer n'appelle pas l'API. Indiquez l'URL ou le fichier du
document OpenAPI, et non simplement l'URL d'une page Swagger UI.

Si la commande affiche le message
`[ERR] Failed to load spec dashboard/sample-swagger.yaml: Cannot parse OpenAPI spec from dashboard/sample-swagger.yaml`,
vérifiez d'abord que les dépendances de l'analyzer ont été installées depuis
la racine du dépôt dans Git Bash, avec le même interpréteur Python que celui
utilisé pour exécuter l'analyzer :

```bash
python -m pip install -r scripts/requirements.txt
```

Relancez ensuite la commande d'analyse.

Si vous avez des questions sur [scripts/start.sh](../../scripts/start.sh) ou
ses paramètres, consultez le [guide HOWTO](./HOWTO.md).

### 2.2 Ouvrir et commenter le rapport

Une fois l'analyse terminée, ouvrez `dashboard/index.html` dans un navigateur
si la page ne s'ouvre pas automatiquement. Le rapport généré est enregistré
dans `reports/latest-report.json`.

Discutez des informations qui peuvent être évaluées à partir de la
spécification et des mesures qui nécessitent une API en cours d'exécution. Les
résultats du mode Swagger seul sont basés sur le contrat : ils ne correspondent
pas à des mesures réelles du temps de réponse ou de la taille des charges utiles.

---

## Partie 3 — Générer un rapport Green Score pour une application existante

Utilisez une application déjà en cours d'exécution, qu'elle soit écrite en
Java, .NET ou Python;

### 3.1 Vérifier l'accessibilité de l'application et de sa spécification Swagger

Démarrez l'application en suivant ses instructions habituelles. Avant
d'exécuter l'analyzer, identifiez :

- l'URL de base de l'application ainsi qu'un point de terminaison de santé ou un autre point de terminaison censé répondre ;
- l'URL menant vers le swagger en JSON/YAML (par exemple, `/v3/api-docs`, `/swagger/v1/swagger.json` ou `/openapi.json`).

Dans Git Bash, vérifiez que les deux URL répondent. Remplacez les URL d'exemple
par celles de votre application :

```bash
curl -f "http://localhost:8080/health"
curl -f "http://localhost:8080/v3/api-docs"
```

Le chemin de santé dépend de l'application. Si l'application ou le chemin vers son swagger est protégée, assurez-vous de disposer des autorisations
nécessaires avant de continuer.

### 3.2 Lancer l'analyse sur l'application

Indiquez à la fois l'URL de base de l'application en cours d'exécution et
l'URL menant au swagger. Adaptez les URL et le nom de l'application à
votre configuration :

```bash
bash scripts/start.sh \
  --target http://localhost:8080 \
  --swagger http://localhost:8080/v3/api-docs \
  --appname my-application
```

L'analyzer peut maintenant mesurer les points de terminaison décrits dans la
spécification. Ouvrez `dashboard/index.html` dans un navigateur pour consulter
le rapport Green Score (`reports/latest-report.json`).

---

## Partie 4 — Analyser le code source avec Creedengo

[Creedengo](https://green-code-initiative.org/) complète les analyses précédentes : il recherche des règles
d'éco-conception dans le **code source** (Java, Python ou C#). L'API Green Score, elle, évalue le swagger ainsi que le comportement réel de
l'API (Partie 3). Les deux analyses produisent des résultats distincts. L'API n'a pas
besoin d'être démarrée pour cette partie.

Cette partie nécessite Docker ou Podman, utilisé pour lancer
SonarQube, ainsi qu'un dossier / repo Git contenant le code source à analyser. Utilisez le
script habituel `scripts/start.sh` avec `--creedengo`. L'exemple ci-dessous
analyse le swagger de démonstration en mode `swagger-only` avec Creedengo. Remplacez les différents paramètres du script par rapport à votre swagger et votre projet :

```bash
bash scripts/start.sh \
  --swagger dashboard/sample-swagger.yaml \
  --source-dir samples/java-spring \
  --appname example-java-sample
  --creedengo
```
Vous pouvez également faire des tests avec les projets en [Java](../../samples/java-spring/), [Python](../../samples/python-fastapi/) et [.NET](../../samples/csharp-aspnet/) disponibles dans ce repo.  Vous pouvez aussi
indiquer un dépôt Git accessible ➡️ `start.sh` le clone et active Creedengo (exemple en Java 21):

```bash
 bash scripts/start.sh \
 --swagger dashboard/sample-swagger.yaml \
 --git-repo https://github.com/felix-seifert/java-21-maven-project.git \
 --appname example-java-21 \
 --creedengo
```

Ouvrez le dashboard sur votre navigateur pour examiner le résultat, puis discutez des constats
prioritaires et des améliorations possibles. 


---

## Bonus — Pipeline CI

Intégrez l'analyzer au pipeline de votre projet (Azure DevOps ou GitHub
Actions). Consultez les modèles dans [`templates/ci`](../../templates/ci) et
[CI-INTEGRATION.md](CI-INTEGRATION.md).

Le pipeline (`pr-green-api-axa.yml`) :

- s'exécute sur les **pull requests** et **chaque semaine** (le dimanche) ;
- installe JDK 17+, Maven et Python ;
- clone l'analyzer ;
- exécute `scripts/start.sh` avec les paramètres indiqués ;
- analyse Creedengo, Green Score et OpenAPI.

### Recommandations

| Sujet | Vérifications à effectuer |
|-------|---------------------------|
| Variables | Vérifiez que `TARGETS`, `SWAGGER_URL`, `STACK` et `BUILD_AND_RUN` sont définies. |
| Accessibilité de Swagger | Vérifiez que l'agent CI peut s'authentifier et obtenir une réponse `200` du document OpenAPI. |
| Modules | Vérifiez les noms des modules Maven/Gradle et le sous-répertoire ciblé (`JAVA_MODULE`). |
| Secrets | Placez `API_TOKEN`, `CLIENT_SECRET`, etc. dans les variables **secrètes** du CI, jamais dans le fichier YAML ni dans les journaux. |

- [ ] Pipeline ajouté sur une branche distincte
- [ ] Première exécution réussie.
- [ ] Rapport / tableau de bord publié comme artefact.

---

## Dépannage général

| Problème | Solution |
|----------|----------|
| `start.sh` ne s'exécute pas | Utilisez Git Bash, obligatoire pour cet atelier ; n'utilisez pas PowerShell, l'invite de commandes ou WSL. |
| Environnement d'exécution Python ou dépendance manquante | Vérifiez que Python 3.10+ est installé, puis relancez `python -m pip install -r scripts/requirements.txt` depuis la racine du dépôt. |
| L'analyse Swagger seule ne parvient pas à charger la spécification | Vérifiez que `--swagger` pointe vers un document OpenAPI JSON/YAML accessible ou un fichier local valide. |
| L'application en cours d'exécution est inaccessible | Vérifiez que l'application est démarrée et que l'URL de base et le port sont corrects. |
| Le document OpenAPI est inaccessible | Vérifiez l'URL du document, les exigences d'authentification et qu'il renvoie une réponse indiquant une réussite. |
| Scores très faibles pour l'ensemble des règles | Vérifiez les codes d'état HTTP dans le rapport ; les points de terminaison protégés peuvent renvoyer `401` ou `403`. |
| Informations complémentaires | Relancez l'analyse avec `--debug`. |

---

## Ressources

- [README du projet](../../README.md) · [HOWTO](HOWTO.md) · [Intégration CI](CI-INTEGRATION.md)
- [`dashboard/`](../../dashboard) : tableau de bord existant et exemple de spécification OpenAPI
- Grille [**API GreenScore v1.2** (PDF)](https://cdn.digitevent.com/69243f238739dbd18f49846f/websiteBtnFileUrl/0c90ba15-f0d0-4b1a-9fb4-ebd8dfb1717c-71-48-cat-sustainable-api-greenscore-v1-2.pdf)
- [Sobri-IT](https://sobri-it.axa-fr.intraxa/)
- Diapositives de l'atelier : consultez [atelier-project-structure.html](../../atelier-project-structure.html).
