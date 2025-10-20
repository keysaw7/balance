# Configuration OpenAI pour BALANCE

## Vue d'ensemble

BALANCE utilise l'API OpenAI (modèle `gpt-4o-mini`) pour normaliser intelligemment les idées citoyennes. Cette normalisation permet de regrouper des idées similaires exprimées différemment.

### Exemple de normalisation

| Texte original | Normalisation IA |
|----------------|------------------|
| "je voudrais un grand parc avec des jeux pour enfants et des arbres" | Création espaces verts |
| "on a besoin de plus d'aires de jeux" | Création espaces verts |
| "vélo sécurisé pour les enfants" | Développement pistes cyclables |
| "pistes cyclables protégées" | Développement pistes cyclables |

## Configuration

### 1. Obtenir une clé API OpenAI

1. Créer un compte sur [OpenAI Platform](https://platform.openai.com/)
2. Aller dans **API Keys** : <https://platform.openai.com/api-keys>
3. Cliquer sur **Create new secret key**
4. Copier la clé (elle commence par `sk-...`)

### 2. Ajouter la clé à votre environnement

Créer un fichier `.env` à la racine du projet :

```bash
OPENAI_API_KEY=sk-votre-clé-ici
```

**⚠️ Important** : Ne jamais committer ce fichier ! Il est déjà dans `.gitignore`.

### 3. Redémarrer les services

```bash
make dev
```

## Fonctionnement

### Avec clé API (recommandé)

Lorsqu'une clé OpenAI est configurée :

1. L'idée est envoyée à `gpt-4o-mini`
2. Le modèle retourne une version normalisée (3-5 mots)
3. Les idées similaires sont automatiquement regroupées

**Coût estimé** : ~$0.0001 par idée (environ 10 000 idées pour $1)

### Sans clé API (fallback)

Si aucune clé n'est configurée, le système utilise des **règles simples** :

- Mots-clés détectés → Normalisation prédéfinie
- Exemples : "piscine" → "Construction piscine municipale"

**Limitations** :
- ❌ Moins précis
- ❌ Ne comprend pas les synonymes
- ❌ Limité aux mots-clés français

## Modèle utilisé

| Paramètre | Valeur | Raison |
|-----------|--------|--------|
| Modèle | `gpt-4o-mini` | Rapide, économique, performant |
| Temperature | `0.3` | Faible créativité, cohérence élevée |
| Max tokens | `20` | Réponses courtes uniquement |

## Monitoring

Surveiller l'utilisation dans le [Dashboard OpenAI](https://platform.openai.com/usage).

## Sécurité

- ✅ La clé API est chargée via variable d'environnement
- ✅ Jamais exposée côté client
- ✅ Timeout de 10 secondes sur les appels
- ✅ Fallback automatique en cas d'erreur

## Améliorations futures

1. **Cache Redis** : Éviter les appels répétés pour les mêmes textes
2. **Fine-tuning** : Entraîner un modèle spécifique aux idées citoyennes
3. **Multilingual** : Support de plusieurs langues
4. **Embeddings** : Détection de similarité sémantique avancée

## Dépannage

### Erreur "OpenAI API error: 401"

→ Clé API invalide ou expirée. Vérifier sur platform.openai.com

### Erreur "OpenAI API error: 429"

→ Limite de taux dépassée. Attendre ou augmenter le quota.

### Les idées ne sont pas normalisées

→ Vérifier les logs Docker :

```bash
docker logs balance-api-gateway-1 | grep OpenAI
```

Si vous voyez "OpenAI API key not found", la clé n'est pas chargée.

## Support

Pour toute question : ouvrir une issue sur GitHub ou consulter la [documentation OpenAI](https://platform.openai.com/docs/).

