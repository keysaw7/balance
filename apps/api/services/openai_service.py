"""
Service OpenAI pour normaliser les idées citoyennes
Utilise gpt-4o-mini pour une normalisation efficace et rapide
Avec cache Redis pour optimiser les coûts
"""
import os
from typing import Optional
import httpx
from services.redis_service import get_normalized_from_cache, save_normalized_to_cache
from services.language_service import detect_language, get_normalization_prompt

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


async def normalize_idea_with_ai(text: str, use_cache: bool = True) -> str:
    """
    Normalise une idée citoyenne en utilisant OpenAI gpt-4o-mini.
    Utilise Redis pour mettre en cache les résultats et réduire les coûts.
    
    Args:
        text: Texte brut de l'idée citoyenne
        use_cache: Utiliser le cache Redis (True par défaut)
        
    Returns:
        Version normalisée de l'idée (3-5 mots, style: "Action + Sujet")
    """
    # 1. Vérifier le cache Redis
    if use_cache:
        cached = await get_normalized_from_cache(text)
        if cached:
            return cached
    
    # 2. Si pas de clé API, fallback
    if not OPENAI_API_KEY:
        result = normalize_idea_fallback(text)
        if use_cache:
            await save_normalized_to_cache(text, result)
        return result
    
    # 3. Détecter la langue
    language = detect_language(text)
    system_prompt, user_prompt_template = get_normalization_prompt(language)
    
    user_prompt = user_prompt_template.format(text=text)
    
    print(f"🌍 Langue détectée: {language} pour '{text[:50]}...')")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                OPENAI_API_URL,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",  # Rapide et économique
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ],
                    "temperature": 0.3,  # Peu de créativité, plus de cohérence
                    "max_tokens": 20,  # Court
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                normalized = data["choices"][0]["message"]["content"].strip()
                # Nettoyer la réponse
                normalized = normalized.strip('"').strip("'").strip()
                result = normalized if normalized else normalize_idea_fallback(text)
                
                # 3. Sauvegarder dans le cache
                if use_cache:
                    await save_normalized_to_cache(text, result)
                
                return result
            else:
                print(f"OpenAI API error: {response.status_code}")
                result = normalize_idea_fallback(text)
                if use_cache:
                    await save_normalized_to_cache(text, result)
                return result
                
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        result = normalize_idea_fallback(text)
        if use_cache:
            await save_normalized_to_cache(text, result)
        return result


def normalize_idea_fallback(text: str) -> str:
    """
    Normalisation par règles simples (fallback si OpenAI indisponible).
    """
    text_lower = text.lower().strip()
    
    # Dictionnaire de normalisation
    normalizations = {
        # Piscines
        ('piscine', 'piscine municipale', 'construire une piscine', 'je veux une piscine'): 
            'Construction piscine municipale',
        
        # Pistes cyclables
        ('piste cyclable', 'pistes cyclables', 'vélo', 'plus de vélos', 'vélo sécurisé'):
            'Développement pistes cyclables',
        
        # Espaces verts
        ('espace vert', 'parc', 'jardin public', 'espaces verts'):
            'Création espaces verts',
        
        # Pollution
        ('pollution', 'réduire la pollution', 'air pur', 'qualité de l\'air'):
            'Réduction pollution atmosphérique',
        
        # Transports
        ('transport', 'bus', 'métro', 'tramway', 'transport en commun'):
            'Amélioration transports en commun',
    }
    
    # Recherche de correspondance
    for keywords, normalized in normalizations.items():
        if any(keyword in text_lower for keyword in keywords):
            return normalized
    
    # Si pas de correspondance, capitaliser simplement
    words = text.split()
    if len(words) > 5:
        # Prendre les 5 premiers mots
        text = ' '.join(words[:5])
    return text.capitalize()

