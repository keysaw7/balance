"""
Service Redis pour cache et optimisation des performances
"""
import os
import redis.asyncio as redis
from typing import Optional
import hashlib
import json

# Configuration Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis_client: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    """
    Obtenir le client Redis (singleton).
    """
    global redis_client
    
    if redis_client is None:
        redis_client = redis.from_url(
            REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    
    return redis_client


async def close_redis():
    """
    Fermer la connexion Redis.
    """
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


def generate_cache_key(prefix: str, data: str) -> str:
    """
    Génère une clé de cache unique basée sur le contenu.
    """
    hash_value = hashlib.md5(data.lower().encode()).hexdigest()
    return f"{prefix}:{hash_value}"


async def get_normalized_from_cache(text: str) -> Optional[str]:
    """
    Récupère une normalisation depuis le cache Redis.
    
    Args:
        text: Texte original de l'idée
        
    Returns:
        Texte normalisé si trouvé dans le cache, None sinon
    """
    try:
        client = await get_redis()
        key = generate_cache_key("normalize", text)
        cached = await client.get(key)
        
        if cached:
            print(f"✅ Cache HIT pour: {text[:50]}...")
            return cached
        else:
            print(f"❌ Cache MISS pour: {text[:50]}...")
            return None
            
    except Exception as e:
        print(f"Redis get error: {e}")
        return None


async def save_normalized_to_cache(text: str, normalized: str, ttl: int = 86400 * 30):
    """
    Sauvegarde une normalisation dans le cache Redis.
    
    Args:
        text: Texte original
        normalized: Texte normalisé
        ttl: Durée de vie en secondes (défaut: 30 jours)
    """
    try:
        client = await get_redis()
        key = generate_cache_key("normalize", text)
        await client.setex(key, ttl, normalized)
        print(f"💾 Saved to cache: {text[:50]}... → {normalized}")
        
    except Exception as e:
        print(f"Redis set error: {e}")


async def get_cache_stats() -> dict:
    """
    Récupère les statistiques du cache.
    """
    try:
        client = await get_redis()
        info = await client.info("stats")
        
        return {
            "keyspace_hits": info.get("keyspace_hits", 0),
            "keyspace_misses": info.get("keyspace_misses", 0),
            "hit_rate": round(
                info.get("keyspace_hits", 0) / 
                max(info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0), 1) * 100,
                2
            )
        }
    except Exception as e:
        print(f"Redis stats error: {e}")
        return {"error": str(e)}


async def clear_normalization_cache():
    """
    Vide tout le cache de normalisation (utile pour recalculer).
    """
    try:
        client = await get_redis()
        # Récupérer toutes les clés de normalisation
        keys = []
        async for key in client.scan_iter(match="normalize:*"):
            keys.append(key)
        
        if keys:
            await client.delete(*keys)
            return {"deleted": len(keys)}
        else:
            return {"deleted": 0}
            
    except Exception as e:
        print(f"Redis clear error: {e}")
        return {"error": str(e)}

