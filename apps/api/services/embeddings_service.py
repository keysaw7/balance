"""
Service d'embeddings pour détecter la similarité sémantique entre idées
Utilise OpenAI text-embedding-3-small pour des embeddings de qualité
"""
import os
from typing import List, Tuple, Optional
import httpx
import numpy as np
from services.redis_service import get_redis

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"


async def get_embedding(text: str) -> Optional[List[float]]:
    """
    Génère un embedding pour un texte via OpenAI.
    
    Args:
        text: Texte à convertir en embedding
        
    Returns:
        Vecteur d'embedding (1536 dimensions pour text-embedding-3-small)
    """
    if not OPENAI_API_KEY:
        return None
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                OPENAI_EMBEDDINGS_URL,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "text-embedding-3-small",  # Plus petit et rapide
                    "input": text,
                    "encoding_format": "float"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["data"][0]["embedding"]
            else:
                print(f"Embeddings API error: {response.status_code}")
                return None
                
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return None


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calcule la similarité cosinus entre deux vecteurs.
    
    Returns:
        Score de similarité entre 0 et 1 (1 = identique)
    """
    a = np.array(vec1)
    b = np.array(vec2)
    
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


async def find_similar_ideas(
    text: str,
    existing_ideas: List[Tuple[str, str]],  # [(id, normalized_text)]
    threshold: float = 0.85
) -> Optional[Tuple[str, float]]:
    """
    Trouve l'idée la plus similaire parmi les existantes.
    
    Args:
        text: Nouvelle idée
        existing_ideas: Liste des idées existantes (id, texte normalisé)
        threshold: Seuil de similarité minimum (défaut 0.85 = très similaire)
        
    Returns:
        (id, score) de l'idée la plus similaire si > threshold, sinon None
    """
    if not OPENAI_API_KEY or not existing_ideas:
        return None
    
    # 1. Obtenir l'embedding de la nouvelle idée
    new_embedding = await get_embedding(text)
    if not new_embedding:
        return None
    
    # 2. Comparer avec toutes les idées existantes
    best_match = None
    best_score = 0.0
    
    for idea_id, idea_text in existing_ideas:
        # Obtenir l'embedding de l'idée existante (devrait être en cache)
        existing_embedding = await get_embedding(idea_text)
        
        if existing_embedding:
            score = cosine_similarity(new_embedding, existing_embedding)
            
            if score > best_score:
                best_score = score
                best_match = idea_id
    
    # 3. Retourner si au-dessus du seuil
    if best_score >= threshold:
        print(f"✅ Similarité trouvée: {best_score:.3f} (seuil: {threshold})")
        return (best_match, best_score)
    else:
        print(f"❌ Pas de similarité suffisante (meilleur: {best_score:.3f})")
        return None


async def cache_embedding(text: str, embedding: List[float], ttl: int = 86400 * 90):
    """
    Cache un embedding dans Redis pour éviter les recalculs.
    
    Args:
        text: Texte original
        embedding: Vecteur d'embedding
        ttl: Durée de vie (défaut: 90 jours)
    """
    try:
        import json
        import hashlib
        
        client = await get_redis()
        key = f"embedding:{hashlib.md5(text.encode()).hexdigest()}"
        
        # Sérialiser l'embedding en JSON
        await client.setex(key, ttl, json.dumps(embedding))
        
    except Exception as e:
        print(f"Redis embedding cache error: {e}")


async def get_cached_embedding(text: str) -> Optional[List[float]]:
    """
    Récupère un embedding depuis le cache Redis.
    """
    try:
        import json
        import hashlib
        
        client = await get_redis()
        key = f"embedding:{hashlib.md5(text.encode()).hexdigest()}"
        
        cached = await client.get(key)
        if cached:
            return json.loads(cached)
        
        return None
        
    except Exception as e:
        print(f"Redis embedding get error: {e}")
        return None

