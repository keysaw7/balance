# BALANCE MVP - Interface Citoyenne

## 🎯 Objectif

Récolter les idées, revendications et envies des citoyens par ville/pays, avec normalisation automatique par IA.

## ✅ Fonctionnalités Implémentées

### 1. Sélection du Cadre
- **Pays** : France, Belgique, Suisse, Canada, Luxembourg
- **Villes** : Liste prédéfinie par pays
- **Géolocalisation** : Option pour accélérer la sélection

### 2. Soumission d'Idées
- **Zone de saisie** simple et épurée
- **Exemples** pour guider l'utilisateur
- **Validation** : 500 caractères max
- **Anonyme** : pas d'authentification requise

### 3. Visualisation des Idées
- **Stats globales** : nombre d'idées uniques et contributions totales
- **Liste triée** : par popularité (nombre de personnes)
- **Graphique** : barre de progression visuelle
- **Normalisation IA** : fusion automatique des idées similaires

### 4. Normalisation IA

**Principe** : Deux personnes qui expriment la même idée différemment verront leur contribution fusionnée.

**Exemples** :
- "je veux une piscine" + "une piscine" → **"Construction piscine municipale"**
- "piste cyclable" + "plus de vélos" → **"Développement pistes cyclables"**
- "pollution" + "air pur" → **"Réduction pollution atmosphérique"**

**Implémentation actuelle** : Dictionnaire de règles simples
**Évolution future** : LLM pour normalisation intelligente

## 🏗️ Architecture

```
┌─────────────┐
│  Interface  │  Next.js + React + Tailwind CSS
│     Web     │  Port 3000
└──────┬──────┘
       │
       ↓
┌─────────────┐
│     API     │  FastAPI
│   Gateway   │  Port 8000
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Idées     │  En mémoire (temporaire)
│  (Store)    │  → PostgreSQL (à venir)
└─────────────┘
```

## 📊 Modèle de Données

### Idée

```typescript
{
  id: string              // Hash unique basé sur normalized + lieu
  text: string            // Texte original de l'utilisateur
  normalized: string      // Version normalisée par l'IA
  count: number          // Nombre de personnes ayant soumis cette idée
  country: string        // Pays
  city: string          // Ville
  createdAt: string     // Date de première soumission
}
```

## 🚀 Comment Utiliser

### 1. Lancer l'environnement

```bash
make dev
```

### 2. Accéder à l'interface

- **Interface** : http://localhost:3000
- **API** : http://localhost:8000/docs

### 3. Tester le flux

1. Choisir pays → ville
2. Écrire une idée (ex: "une piscine")
3. Cliquer sur "Partager mon idée"
4. Voir les idées proposées → l'idée est normalisée

## 🔄 Flux Utilisateur

```
[Page d'accueil]
     ↓
[Sélection Pays] → Bouton géolocalisation
     ↓
[Sélection Ville]
     ↓
[Saisie Idée] ←→ [Voir les Idées]
```

## 📁 Structure des Fichiers

```
apps/
├── web/
│   ├── pages/
│   │   ├── index.tsx        # Sélection pays/ville
│   │   └── ideas.tsx        # Saisie + visualisation
│   └── styles/
│       └── globals.css      # Tailwind CSS
│
└── api/
    ├── main.py              # Point d'entrée FastAPI
    └── routes/
        └── ideas.py         # Endpoints idées + normalisation
```

## 🎨 Design

- **Minimaliste** : Focus sur l'essentiel
- **Moderne** : Tailwind CSS + gradients
- **Responsive** : Mobile-first
- **Accessible** : Contrastes élevés, textes clairs

## 🔮 Prochaines Étapes

### Court terme
1. **Base de données PostgreSQL** : Persister les idées
2. **Améliorer normalisation** : Intégrer un LLM (GPT-4, Claude)
3. **Plus de villes** : API de géolocalisation complète

### Moyen terme
4. **Authentification optionnelle** : Suivre ses idées
5. **Notifications** : Quand une idée devient populaire
6. **Modération** : Filtrage contenu inapproprié

### Long terme
7. **Analyse Zeus** : Utiliser les idées pour analyse IA
8. **Gouvernance** : Vote sur les idées prioritaires
9. **API publique** : Accès aux données agrégées

## 🧪 Tests

### Test Manuel

```bash
# Soumettre une idée
curl -X POST http://localhost:8000/api/ideas \
  -H "Content-Type: application/json" \
  -d '{"text":"piscine","country":"France","city":"Paris"}'

# Récupérer les idées
curl http://localhost:8000/api/ideas?country=France&city=Paris

# Stats globales
curl http://localhost:8000/api/ideas/stats
```

## 💡 Notes Techniques

### Normalisation IA

Le système actuel utilise un dictionnaire de mots-clés. Pour passer à un LLM :

1. Intégrer OpenAI API ou Anthropic
2. Prompt : "Normalise cette idée citoyenne en 3-5 mots concis"
3. Cache les normalisations pour réduire coûts API
4. Fallback sur règles si API indisponible

### Performances

- **En mémoire** : Instantané, mais perd données au redémarrage
- **PostgreSQL** : Ajouter index sur `(country, city, normalized)`
- **Redis** : Cache pour agrégations fréquentes

### Sécurité

- **Rate limiting** : Limiter soumissions par IP
- **Validation** : Longueur max, caractères autorisés
- **Modération** : Blacklist mots interdits

## 📝 Licence

MIT - Open Source

