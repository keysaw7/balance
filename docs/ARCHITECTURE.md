# Architecture BALANCE

## Vue d'ensemble

BALANCE est une plateforme d'intelligence collective composée de plusieurs services microservices orchestrés via Docker.

## Diagramme d'architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     UTILISATEURS                            │
│  (Citoyens, Experts, Administrateurs, Chercheurs)          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                  NGINX (Reverse Proxy)                      │
│                  Port 80/443                                │
└─────┬───────────────────────────────────┬───────────────────┘
      │                                   │
      ↓                                   ↓
┌─────────────────┐              ┌──────────────────────────┐
│   WEB APP       │              │    API GATEWAY           │
│   (Next.js)     │◄─────────────│    (FastAPI)             │
│   Port 3000     │              │    Port 8000             │
└─────────────────┘              └────┬─────────────────────┘
                                      │
                   ┌──────────────────┼──────────────────┐
                   │                  │                  │
                   ↓                  ↓                  ↓
         ┌─────────────────┐ ┌──────────────┐ ┌─────────────────┐
         │  ZEUS SERVICE   │ │ DATA SERVICE │ │ GOV SERVICE     │
         │  (PyTorch + AI) │ │ (Analytics)  │ │ (Démocratie)    │
         │  Port 8001      │ │ Port 8002    │ │ Port 8003       │
         └────────┬────────┘ └──────┬───────┘ └────────┬────────┘
                  │                 │                   │
                  └─────────────────┼───────────────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ↓                 ↓                 ↓
         ┌─────────────┐   ┌──────────────┐  ┌──────────────┐
         │ PostgreSQL  │   │    Redis     │  │  Prometheus  │
         │ Port 5432   │   │  Port 6379   │  │  Port 9090   │
         └─────────────┘   └──────────────┘  └──────────────┘
```

## Services

### 1. Interface Web (Next.js)
**Responsabilité** : Interface utilisateur pour les citoyens

**Fonctionnalités** :
- Page d'accueil et présentation
- Formulaire de soumission de problématique
- Visualisation des analyses Zeus
- Dashboard utilisateur
- Système de vote et feedback
- Interface de gouvernance

**Technologies** :
- Next.js 14
- React 18
- Tailwind CSS
- TypeScript

### 2. API Gateway (FastAPI)
**Responsabilité** : Point d'entrée unifié pour tous les services backend

**Fonctionnalités** :
- Routage des requêtes vers les services
- Authentification et autorisation
- Rate limiting
- Validation des données
- Logging centralisé

**Technologies** :
- FastAPI
- Pydantic
- Python-JOSE (JWT)
- SQLAlchemy

### 3. Zeus Service (PyTorch)
**Responsabilité** : Moteur d'IA pour l'analyse de politiques publiques

**Fonctionnalités** :
- Analyse multi-critères des problématiques
- Génération de scénarios optimaux
- Simulation d'impact
- Explication des recommandations (XAI)
- Optimisation Pareto

**Technologies** :
- PyTorch
- Transformers (Hugging Face)
- Optuna (hyperparameter tuning)
- Scikit-learn

**État actuel** : Architecture préparée, implémentation en attente de ressources

### 4. Data Service
**Responsabilité** : Gestion et traitement des données

**Fonctionnalités** :
- Ingestion de données publiques
- Anonymisation et confidentialité
- Agrégation et statistiques
- Export et visualisation
- API de données

**Technologies** :
- FastAPI
- Pandas
- PostgreSQL

### 5. Governance Service
**Responsabilité** : Système de gouvernance démocratique

**Fonctionnalités** :
- Gestion des propositions
- Système de vote
- Référendum technique
- Audit et transparence
- Historique des décisions

**Technologies** :
- FastAPI
- SQLAlchemy
- Redis (cache)

### 6. Infrastructure

#### PostgreSQL
- Base de données principale
- Stockage des problématiques, analyses, utilisateurs
- Schéma normalisé

#### Redis
- Cache distribué
- File d'attente (Celery)
- Sessions utilisateur

#### Prometheus + Grafana
- Monitoring des services
- Métriques de performance
- Alertes

## Flux de données

### 1. Soumission d'une problématique

```
Utilisateur → Web App → API Gateway → Validation
                                    ↓
                            Data Service (stockage)
                                    ↓
                            Zeus Service (analyse)
                                    ↓
                            Résultats → PostgreSQL
                                    ↓
                            Notification → Utilisateur
```

### 2. Consultation des résultats

```
Utilisateur → Web App → API Gateway → Data Service
                                    ↓
                            PostgreSQL (requête)
                                    ↓
                            Formatage → JSON
                                    ↓
                            Web App (visualisation)
```

### 3. Vote de gouvernance

```
Utilisateur → Web App → API Gateway → Gov Service
                                    ↓
                            Validation + Stockage
                                    ↓
                            Redis (cache des votes)
                                    ↓
                            Résultat agrégé → Dashboard
```

## Modèles de données

### Problématique

```typescript
{
  id: string
  titre: string
  description: string
  domaine: string  // climat, santé, éducation...
  région: string   // local, national, europe...
  contraintes: {
    budget: number
    délai: string
    priorités: string[]
  }
  auteur_id: string
  statut: 'soumise' | 'en_analyse' | 'analysée' | 'archivée'
  créée_le: timestamp
  mise_à_jour_le: timestamp
}
```

### Analyse Zeus

```typescript
{
  id: string
  problématique_id: string
  scénarios: Scenario[]
  méthodologie: string
  confiance: number  // 0-1
  explications: string[]
  graphiques: {
    pareto: object
    impacts: object
    timeline: object
  }
  analysé_le: timestamp
}
```

### Scénario

```typescript
{
  id: string
  titre: string
  description: string
  score_global: number
  trade_offs: {
    critère: string
    impact: string
    justification: string
  }[]
  coût_implémentation: number
  timeline: string
  impacts: {
    économique: number
    social: number
    environnemental: number
  }
}
```

### Utilisateur

```typescript
{
  id: string
  email: string
  pseudonyme: string
  rôle: 'citoyen' | 'expert' | 'admin'
  préférences: {
    domaines: string[]
    régions: string[]
    notifications: boolean
  }
  créé_le: timestamp
}
```

## Sécurité

### Authentification
- JWT tokens (access + refresh)
- Durée de vie : 15min (access), 7 jours (refresh)
- Stockage : httpOnly cookies

### Autorisation
- RBAC (Role-Based Access Control)
- Niveaux : citoyen, expert, modérateur, admin

### Données sensibles
- Chiffrement en transit (HTTPS)
- Chiffrement au repos (PostgreSQL)
- Anonymisation automatique
- Consentement granulaire RGPD

### Rate Limiting
- 100 requêtes/minute par IP (général)
- 10 soumissions/jour par utilisateur
- 1000 requêtes/heure pour l'API

## Performance

### Caching
- Redis pour les résultats fréquents
- Cache CDN pour les assets statiques
- Cache navigateur (service worker)

### Scalabilité
- Services stateless
- Réplication PostgreSQL (read replicas)
- Load balancing Nginx
- Kubernetes ready

## Monitoring

### Métriques clés
- Temps de réponse API (< 200ms p95)
- Disponibilité (> 99.9%)
- Erreurs (< 0.1%)
- Utilisation ressources (CPU, RAM, Disk)

### Alertes
- Service down
- Erreur rate > seuil
- Latence > seuil
- Disk > 80%

## Prochaines étapes

### Phase 1 : MVP (en cours)
- ✅ Infrastructure Docker
- ✅ Services de base
- 🔄 Interface web complète
- ⏳ Intégration API

### Phase 2 : Fonctionnalités core
- Authentification
- Soumission de problématiques
- Visualisation basique
- Gouvernance MVP

### Phase 3 : Zeus (nécessite ressources)
- Modèle d'IA de base
- Analyse simple
- Génération de scénarios
- Explications

### Phase 4 : Avancé
- Zeus complet avec ML
- Optimisation multi-objectifs
- Système de vote avancé
- Mobile app

