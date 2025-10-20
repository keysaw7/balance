# BALANCE - Présentation du Projet

## 🎯 Pitch (30 secondes)

**BALANCE** est une plateforme citoyenne open-source qui permet de **recueillir et analyser les idées de la population** grâce à l'intelligence artificielle multilingue.

Les idées similaires sont **automatiquement fusionnées** pour créer une vision claire des priorités citoyennes.

---

## 🚀 Démo Rapide

```bash
# 1. Cloner le projet
git clone https://github.com/keysaw7/balance.git
cd balance

# 2. Ajouter votre clé OpenAI (optionnel)
echo "OPENAI_API_KEY=sk-votre-clé" > .env

# 3. Lancer l'application
make dev

# 4. Ouvrir dans le navigateur
open http://localhost:3000
```

**C'est tout !** Docker gère toute l'infrastructure.

---

## 💡 Cas d'Usage

### Pour les Citoyens
- 📝 **Soumettre des idées** en quelques secondes
- 🌍 **N'importe quelle ville** dans le monde
- 🌐 **Dans leur langue** (FR/EN/AR)
- 📊 **Voir les priorités** de leur communauté

### Pour les Élus/Mairies
- 📊 **Dashboard des priorités** citoyennes
- 🔍 **Analyse sémantique** des revendications
- 📈 **Tendances en temps réel**
- 🎯 **Décisions basées sur les données**

### Pour les Chercheurs
- 📚 **Données open-source** sur l'opinion publique
- 🧠 **IA multilingue** pour analyse comparative
- 🔬 **Embeddings sémantiques** pour études
- 📊 **Export PostgreSQL** pour recherche

---

## 🎨 Interface

### Étape 1 : Sélection du Lieu
```
┌──────────────────────────────────────┐
│   🌍 BALANCE - Votre voix compte     │
├──────────────────────────────────────┤
│                                      │
│  Choisissez votre pays:              │
│  ┌────────┐  ┌────────┐             │
│  │ France │  │Belgium │  ...        │
│  └────────┘  └────────┘             │
│                                      │
│  ou: [Maroc________________] →       │
│                                      │
└──────────────────────────────────────┘
```

### Étape 2 : Soumission d'Idée
```
┌──────────────────────────────────────┐
│   📍 Casablanca, Maroc               │
├──────────────────────────────────────┤
│                                      │
│  Quelle est votre idée ?             │
│  ┌────────────────────────────────┐ │
│  │ نريد مسبح عمومي مجاني         │ │
│  │                                │ │
│  └────────────────────────────────┘ │
│                      0/500 caractères │
│                                      │
│         [Partager mon idée]          │
│                                      │
└──────────────────────────────────────┘
```

### Étape 3 : Visualisation
```
┌──────────────────────────────────────┐
│   📊 Idées proposées - Casablanca    │
├──────────────────────────────────────┤
│  3 idées uniques  |  5 contributions │
├──────────────────────────────────────┤
│                                      │
│  🏊 إنشاء مسبح عمومي مجاني          │
│     "نريد مسبح..."                  │
│                          👥 2 personnes│
│                                      │
│  🚌 Amélioration transports          │
│     "plus de bus..."                 │
│                          👥 2 personnes│
│                                      │
│  🌳 Création espaces verts           │
│     "un parc avec..."                │
│                          👥 1 personne │
│                                      │
└──────────────────────────────────────┘
```

---

## 🤖 Intelligence Artificielle

### Pipeline de Normalisation

```
Idée brute
    ↓
┌─────────────────────────────┐
│ 1. Détection de langue      │  FR / EN / AR
├─────────────────────────────┤
│ 2. Cache Redis ?            │  ✓ HIT → Retour immédiat
├─────────────────────────────┤
│ 3. OpenAI gpt-4o-mini       │  Normalisation intelligente
├─────────────────────────────┤
│ 4. Embeddings sémantiques   │  Vecteur 1536 dimensions
├─────────────────────────────┤
│ 5. Recherche similarité     │  Cosine > 0.88 = Fusion
├─────────────────────────────┤
│ 6. Sauvegarde cache         │  TTL 30 jours
└─────────────────────────────┘
    ↓
Idée normalisée + fusionnée
```

### Exemples Concrets

| Langue | Texte Original | Normalisation IA |
|--------|---------------|------------------|
| 🇫🇷 | "je voudrais un grand parc avec des jeux pour enfants" | **Création espaces verts** |
| 🇺🇸 | "we need more public transportation in our city" | **Public transportation expansion** |
| 🇸🇦 | "نريد مسبح عمومي مجاني" | **إنشاء مسبح عمومي مجاني** |

---

## 📊 Performance & Coûts

### Latence
| Opération | Sans Cache | Avec Cache | Gain |
|-----------|-----------|-----------|------|
| Normalisation | ~1200ms | ~1ms | **99.9%** |
| Embeddings | ~400ms | ~1ms | **99.7%** |
| Total | ~3500ms | ~2000ms | **43%** |

### Coûts OpenAI
| Volume | Sans Cache | Avec Cache (90% hit) | Économie |
|--------|-----------|---------------------|----------|
| 1,000 idées | $0.12 | $0.012 | **$0.11** |
| 10,000 idées | $1.20 | $0.12 | **$1.08** |
| 100,000 idées | $12.00 | $1.20 | **$10.80** |

---

## 🏗️ Architecture Technique

```
┌─────────────────────────────────────────────────────┐
│                    UTILISATEURS                     │
└───────────────────────┬─────────────────────────────┘
                        │
                        ↓
            ┌───────────────────────┐
            │   Nginx (Port 80)     │
            └───────────┬───────────┘
                        │
        ┌───────────────┴───────────────┐
        ↓                               ↓
┌───────────────┐              ┌───────────────┐
│   Web App     │              │  API Gateway  │
│   Next.js     │◄─────────────│   FastAPI     │
│   Port 3000   │              │   Port 8000   │
└───────────────┘              └───────┬───────┘
                                       │
                    ┌──────────────────┼──────────────┐
                    ↓                  ↓              ↓
            ┌──────────────┐   ┌──────────┐   ┌──────────┐
            │  PostgreSQL  │   │  Redis   │   │  OpenAI  │
            │  Port 5432   │   │ Port 6379│   │   API    │
            └──────────────┘   └──────────┘   └──────────┘
```

### Stack Technologique

**Frontend**
- Next.js 14 + React 18
- TypeScript + Tailwind CSS
- Responsive & Mobile-first

**Backend**
- FastAPI (Python 3.11)
- SQLAlchemy + Alembic
- Async/Await

**IA & ML**
- OpenAI gpt-4o-mini (normalisation)
- text-embedding-3-small (embeddings)
- NumPy (similarité cosinus)

**Infrastructure**
- Docker + Docker Compose
- PostgreSQL 15
- Redis 7 (cache)
- Nginx (reverse proxy)
- Prometheus + Grafana (monitoring)

---

## 🌟 Points Forts

### 1. 🌍 Portée Mondiale
- ✅ **N'importe quelle ville** validée via Nominatim (OpenStreetMap)
- ✅ **3 langues** (FR/EN/AR) avec détection automatique
- ✅ **Coordonnées GPS** pour chaque lieu

### 2. 🤖 IA de Pointe
- ✅ **OpenAI gpt-4o-mini** pour normalisation
- ✅ **Embeddings sémantiques** pour fusion intelligente
- ✅ **Prompts adaptatifs** par langue

### 3. 🚀 Performance
- ✅ **Cache Redis** → 90% réduction coûts
- ✅ **< 2s latence** avec cache
- ✅ **Scalable** (millions d'idées)

### 4. 🔓 Open Source
- ✅ **Code libre** (GitHub)
- ✅ **Documentation complète**
- ✅ **Facilement déployable** (Docker)

### 5. 💰 Économique
- ✅ **$0.00001/idée** avec cache
- ✅ **API gratuite** (Nominatim)
- ✅ **Infrastructure minimale**

---

## 🛠️ Développement

### Structure du Projet
```
balance/
├── apps/
│   ├── web/              # Frontend Next.js
│   │   ├── pages/
│   │   │   ├── index.tsx     # Sélection lieu
│   │   │   └── ideas.tsx     # Soumission + visualisation
│   │   └── styles/
│   └── api/              # Backend FastAPI
│       ├── routes/
│       │   ├── ideas.py      # Endpoints idées
│       │   └── geocoding.py  # Validation villes
│       └── services/
│           ├── openai_service.py
│           ├── redis_service.py
│           ├── embeddings_service.py
│           ├── language_service.py
│           └── geocoding_service.py
├── docs/
│   ├── FEATURES_v0.3.0.md    # Résumé fonctionnalités
│   ├── OPENAI_SETUP.md       # Guide OpenAI
│   └── CHANGELOG.md          # Historique
└── docker-compose.yml
```

### Commandes Utiles
```bash
# Développement
make dev              # Lancer tout
make health          # Vérifier santé services
docker logs balance-api-gateway-1 -f

# Base de données
docker exec balance-postgres-1 psql -U balance -d balance -c "SELECT * FROM ideas;"

# Cache Redis
docker exec balance-redis-1 redis-cli KEYS "*"

# Tests
curl -X POST http://localhost:8000/api/ideas \
  -H "Content-Type: application/json" \
  -d '{"text":"test idea","country":"France","city":"Paris"}'
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | Guide de démarrage rapide |
| [VISION.md](VISION.md) | Vision complète du projet Zeus |
| [FEATURES_v0.3.0.md](docs/FEATURES_v0.3.0.md) | Résumé détaillé des fonctionnalités |
| [OPENAI_SETUP.md](docs/OPENAI_SETUP.md) | Configuration OpenAI |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Architecture technique |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Guide contributeur |
| [CHANGELOG.md](docs/CHANGELOG.md) | Historique des versions |

---

## 🎯 Prochaines Étapes

### Court Terme (v0.4.0)
- [ ] Dashboard admin pour modération
- [ ] Export CSV/JSON des idées
- [ ] Autocomplétion des villes
- [ ] Rate limiting OpenAI

### Moyen Terme (v0.5.0)
- [ ] Support de 10+ langues
- [ ] Système de vote sur les idées
- [ ] Notifications push
- [ ] API GraphQL

### Long Terme (v1.0.0)
- [ ] Zeus AI pour analyse prédictive
- [ ] Intégration élus/mairies
- [ ] Mobile apps (iOS/Android)
- [ ] Blockchain pour traçabilité

---

## 📞 Contact & Contribution

**GitHub** : https://github.com/keysaw7/balance
**Issues** : Pour bugs et suggestions
**Pull Requests** : Bienvenues !

### Contribuer
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add some AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📜 Licence

Ce projet est open-source sous licence MIT.

---

## 🙏 Remerciements

- **OpenAI** pour l'API gpt-4o-mini et embeddings
- **OpenStreetMap** / Nominatim pour la géolocalisation
- **Communauté open-source** pour les outils utilisés

---

**BALANCE v0.3.0** - *Votre voix compte* 🗳️

