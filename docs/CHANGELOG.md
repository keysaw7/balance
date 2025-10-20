# CHANGELOG

## [0.2.0] - 2025-10-20

### 🎨 Interface Utilisateur

#### Sélecteur de lieu amélioré
- ✅ **Saisie libre** : Possibilité d'entrer n'importe quel pays et ville du monde
- ✅ **Suggestions intelligentes** : 10 pays prédéfinis pour une sélection rapide
- ✅ **Validation simple** : Vérification que la ville contient au moins 3 caractères
- ✅ **UX améliorée** : Focus automatique, soumission par Enter, boutons désactivés intelligemment

**Avant** : Liste fixe de 5 pays et villes prédéfinies
**Après** : Tout pays et ville du monde acceptés

### 🤖 Intelligence Artificielle

#### Normalisation OpenAI
- ✅ **Intégration OpenAI API** avec modèle `gpt-4o-mini`
- ✅ **Prompts optimisés** pour générer des expressions normalisées de 3-5 mots
- ✅ **Fallback automatique** sur règles simples si pas de clé API
- ✅ **Timeout de sécurité** à 10 secondes
- ✅ **Gestion d'erreurs robuste**

**Paramètres OpenAI** :
- Modèle : `gpt-4o-mini` (rapide et économique)
- Temperature : `0.3` (cohérence maximale)
- Max tokens : `20` (réponses courtes)

**Coût estimé** : ~$0.0001 par idée

#### Exemples de normalisation

| Texte original | Normalisation |
|----------------|---------------|
| "je voudrais un grand parc avec des jeux pour enfants et des arbres" | Création espaces verts |
| "il faut plus de bus dans ma ville" | Amélioration transports en commun |
| "métro rapide pour tous" | Amélioration transports en commun |

### 📦 Infrastructure

#### Services
- ✅ **Service OpenAI** : Nouveau module `services/openai_service.py`
- ✅ **Variable d'environnement** : `OPENAI_API_KEY` ajoutée au docker-compose
- ✅ **Dépendance** : `openai==1.3.0` ajoutée aux requirements

#### Base de données
- ✅ Les idées normalisées sont fusionnées automatiquement
- ✅ Le compteur `count` s'incrémente pour les idées identiques

### 📚 Documentation

#### Nouveaux documents
- ✅ `docs/OPENAI_SETUP.md` : Guide complet pour configurer OpenAI
- ✅ `docs/CHANGELOG.md` : Historique des modifications
- ✅ README.md mis à jour avec les nouvelles fonctionnalités

### 🧪 Tests réalisés

#### Sélecteur libre
- ✅ Pays personnalisé : "Maroc" → OK
- ✅ Ville personnalisée : "Casablanca" → OK
- ✅ URL encodée correctement : `?country=Maroc&city=Casablanca`

#### Normalisation IA
- ✅ Idée 1 : "parc avec jeux pour enfants" → "Création espaces verts"
- ✅ Idée 2 : "plus de bus" → "Amélioration transports en commun"
- ✅ Idée 3 : "métro rapide" → "Amélioration transports en commun" (count=2) ✅

#### Persistance
- ✅ PostgreSQL stocke correctement les idées normalisées
- ✅ Les compteurs s'incrémentent lors de la fusion
- ✅ Les données sont conservées après redémarrage

---

## [0.1.0] - 2025-10-20

### 🎉 MVP Initial

#### Interface Web
- ✅ Sélection pays/ville
- ✅ Géolocalisation optionnelle
- ✅ Formulaire de soumission d'idées
- ✅ Visualisation des idées avec stats

#### API Backend
- ✅ Endpoint POST `/api/ideas`
- ✅ Endpoint GET `/api/ideas`
- ✅ Normalisation par règles simples
- ✅ CORS configuré

#### Infrastructure
- ✅ Docker Compose multi-services
- ✅ PostgreSQL 15
- ✅ Redis 7
- ✅ Nginx reverse proxy
- ✅ Prometheus + Grafana

#### Documentation
- ✅ VISION.md
- ✅ CONTRIBUTING.md
- ✅ README.md
- ✅ ARCHITECTURE.md

