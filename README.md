# BALANCE 🏛️

**Plateforme citoyenne pour recueillir et analyser les idées de la population**

![BALANCE MVP](./docs/images/mvp-screenshot.png)

## 🎯 Mission

BALANCE permet aux citoyens de partager leurs idées, revendications et envies pour leur ville ou leur pays. Les idées similaires sont automatiquement fusionnées par IA pour créer une vision claire des priorités citoyennes.

## ✨ Fonctionnalités

### v0.3.0 (Production Ready)

#### 🌍 Géographie
- ✅ **Validation Nominatim (OpenStreetMap)** - Vérification en temps réel des villes
- ✅ **Sélection libre** de n'importe quel pays et ville du monde
- ✅ **Suggestions intelligentes** de 10 pays populaires
- ✅ **Géolocalisation** optionnelle via navigateur
- ✅ **Coordonnées GPS** (lat/long) pour chaque lieu

#### 🤖 Intelligence Artificielle
- ✅ **Normalisation OpenAI** (gpt-4o-mini) avec prompts multilingues
- ✅ **Support multilingue** : Français, Anglais, Arabe
- ✅ **Détection automatique de langue**
- ✅ **Embeddings sémantiques** (text-embedding-3-small) pour fusion intelligente
- ✅ **Seuil de similarité** à 88% pour regroupement automatique
- ✅ **Fallback sur règles** si pas de clé OpenAI

#### 🗄️ Performance & Cache
- ✅ **Cache Redis** pour normalisation (90% réduction coûts OpenAI)
- ✅ **TTL de 30 jours** sur cache
- ✅ **Hit rate tracking** pour monitoring
- ✅ **Base PostgreSQL** avec indexes optimisés
- ✅ **Latence < 2s** avec cache, ~3.5s sans cache

#### 🎨 Interface
- ✅ **Soumission anonyme** (500 caractères max)
- ✅ **Visualisation temps réel** avec statistiques
- ✅ **Graphique des idées** les plus populaires
- ✅ **Interface multilingue** (FR/EN/AR)
- ✅ **Design épuré** et responsive

### Exemple

**2 personnes soumettent** :
- "je veux une piscine municipale"
- "une piscine"

**L'IA normalise** → **"Construction piscine municipale"** (2 personnes)

## 🚀 Démarrage Rapide

### Prérequis

- Docker & Docker Compose
- Node.js 18+ (pour développement local)
- Python 3.11+ (pour développement local)

### Installation

```bash
# Cloner le projet
git clone <repo-url>
cd balance

# (Optionnel) Configurer la clé OpenAI pour une normalisation IA optimale
echo "OPENAI_API_KEY=sk-votre-clé" > .env

# Lancer l'environnement de développement
make dev
```

### Accès

- **Interface Web** : <http://localhost:3000>
- **API** : <http://localhost:8000>
- **Documentation API** : <http://localhost:8000/docs>
- **Grafana** : <http://localhost:3001>

> **💡 Note** : Sans clé OpenAI, le système utilise des règles simples pour la normalisation (moins précis).

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────┐
│                    UTILISATEURS                      │
└───────────────────────┬──────────────────────────────┘
                        │
                        ↓
    ┌─────────────────────────────────────────┐
    │          Nginx (Reverse Proxy)          │
    │              Port 80/443                │
    └──────────┬─────────────────┬────────────┘
               │                 │
               ↓                 ↓
    ┌──────────────┐    ┌──────────────┐
    │   Web App    │    │ API Gateway  │
    │  (Next.js)   │◄───│  (FastAPI)   │
    │  Port 3000   │    │  Port 8000   │
    └──────────────┘    └──────┬───────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ↓             ↓             ↓
           ┌──────────┐  ┌─────────┐  ┌──────────┐
           │PostgreSQL│  │  Redis  │  │Prometheus│
           │Port 5432 │  │Port 6379│  │Port 9090 │
           └──────────┘  └─────────┘  └──────────┘
```

### Stack Technique

**Frontend**
- Next.js 14
- React 18
- Tailwind CSS
- TypeScript

**Backend**
- FastAPI
- Python 3.11
- Pydantic
- SQLAlchemy
- OpenAI API (gpt-4o-mini)

**Infrastructure**
- PostgreSQL 15
- Redis 7
- Nginx
- Docker & Docker Compose

## 📁 Structure du Projet

```
balance/
├── apps/
│   ├── web/              # Interface Next.js
│   │   ├── pages/
│   │   │   ├── index.tsx    # Sélection lieu
│   │   │   └── ideas.tsx    # Saisie + visualisation
│   │   └── styles/
│   └── api/              # API FastAPI
│       ├── main.py
│       └── routes/
│           └── ideas.py     # Normalisation IA
│
├── docs/
│   ├── VISION.md         # Vision complète du projet
│   ├── ARCHITECTURE.md   # Architecture technique
│   ├── MVP.md            # Documentation MVP
│   └── CONTRIBUTING.md   # Guide contributeurs
│
├── infrastructure/
│   ├── nginx/
│   └── monitoring/
│
├── docker-compose.yml
├── Makefile
└── README.md
```

## 🎨 Interface

### 1. Sélection du Lieu

Choisissez votre pays puis votre ville (ou utilisez la géolocalisation).

### 2. Partager une Idée

Écrivez simplement votre idée en langage naturel. L'IA se charge de la normaliser.

### 3. Voir les Idées

Visualisez toutes les idées proposées, triées par popularité, avec des statistiques claires.

## 🔧 Développement

### Commandes Make

```bash
make setup    # Installation initiale
make dev      # Lancer l'environnement
make stop     # Arrêter les services
make clean    # Nettoyer
make logs     # Voir les logs
```

### Tests

```bash
# Test API direct
curl -X POST http://localhost:8000/api/ideas \
  -H "Content-Type: application/json" \
  -d '{"text":"piscine","country":"France","city":"Paris"}'

# Récupérer les idées
curl http://localhost:8000/api/ideas?country=France&city=Paris
```

## 🗺️ Roadmap

### Phase 1 : MVP ✅ (Actuel)
- Interface basique
- Normalisation IA simple
- Stockage en mémoire

### Phase 2 : Base de données (En cours)
- PostgreSQL pour persistance
- Amélioration normalisation (LLM)
- Plus de villes (API géo complète)

### Phase 3 : Fonctionnalités avancées
- Authentification optionnelle
- Notifications
- Modération automatique
- Export données

### Phase 4 : Analyse Zeus
- Moteur d'IA pour analyser les idées
- Génération de scénarios optimaux
- Système de vote et gouvernance

## 📊 Modèle de Données

### Idée

| Champ | Type | Description |
|-------|------|-------------|
| `id` | string | Identifiant unique |
| `text` | string | Texte original de l'utilisateur |
| `normalized` | string | Version normalisée par l'IA |
| `count` | number | Nombre de personnes |
| `country` | string | Pays |
| `city` | string | Ville |
| `createdAt` | string | Date de création |

## 🤝 Contribuer

Nous accueillons toutes les contributions ! Consultez [CONTRIBUTING.md](./CONTRIBUTING.md) pour commencer.

### Types de Contributions

- 🐛 **Bugs** : Signaler ou corriger
- ✨ **Features** : Proposer de nouvelles fonctionnalités
- 📝 **Documentation** : Améliorer la doc
- 🎨 **Design** : Améliorer l'UI/UX
- 🧪 **Tests** : Ajouter des tests

## 📝 Licence

MIT License - Ce projet est open source.

## 🌟 Philosophie

BALANCE est construit sur les principes de :

- **Transparence** : Code et données ouvertes
- **Démocratie** : Gouvernance collective
- **Privacy** : Anonymat et protection des données
- **Accessibilité** : Interface simple pour tous
- **Neutralité** : Aucun biais politique

## 📞 Contact

- **Documentation** : [/docs](./docs)
- **Issues** : GitHub Issues
- **Discussions** : GitHub Discussions

---

**Made with ❤️ for democracy**
