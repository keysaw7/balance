"""
Service de géocodage pour valider les villes avec Nominatim (OpenStreetMap)
API gratuite, pas besoin de clé API
"""
import httpx
from typing import Optional, Dict
import asyncio

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_HEADERS = {
    "User-Agent": "BALANCE/0.2.0 (https://github.com/balance-platform/balance)"
}


async def validate_city(city: str, country: str) -> Dict[str, any]:
    """
    Valide qu'une ville existe dans un pays donné via Nominatim.
    Normalise le nom de la ville pour éviter les doublons (casse, accents, etc.)
    
    Args:
        city: Nom de la ville
        country: Nom du pays
        
    Returns:
        {
            "valid": bool,
            "display_name": str,     # Nom complet formaté
            "normalized_name": str,  # Nom normalisé pour la base de données
            "osm_id": str,          # Identifiant unique OpenStreetMap
            "latitude": float,
            "longitude": float,
            "importance": float,
            "postal_code": str      # Code postal si disponible
        }
    """
    if not city.strip() or not country.strip():
        return {"valid": False, "error": "City and country required"}
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                NOMINATIM_URL,
                headers=NOMINATIM_HEADERS,
                params={
                    "q": f"{city}, {country}",
                    "format": "json",
                    "limit": 1,
                    "addressdetails": 1
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if len(data) > 0:
                    result = data[0]
                    
                    # Vérifier que c'est bien une ville/village
                    place_type = result.get("type", "")
                    valid_types = ["city", "town", "village", "municipality", "administrative"]
                    
                    if any(t in place_type for t in valid_types) or result.get("importance", 0) > 0.3:
                        address = result.get("address", {})
                        
                        # Extraire le nom officiel de la ville
                        city_name = (
                            address.get("city") or 
                            address.get("town") or 
                            address.get("village") or 
                            address.get("municipality") or
                            result.get("name")
                        )
                        
                        return {
                            "valid": True,
                            "display_name": result.get("display_name", f"{city}, {country}"),
                            "normalized_name": city_name,  # Nom officiel normalisé
                            "osm_id": str(result.get("osm_id", "")),
                            "latitude": float(result.get("lat", 0)),
                            "longitude": float(result.get("lon", 0)),
                            "importance": float(result.get("importance", 0)),
                            "postal_code": address.get("postcode", ""),
                            "type": place_type
                        }
                
                return {"valid": False, "error": "City not found"}
            else:
                return {"valid": False, "error": f"API error: {response.status_code}"}
                
    except asyncio.TimeoutError:
        # Timeout = on accepte quand même (mode dégradé)
        # Normaliser manuellement pour cohérence
        normalized = city.strip().title()
        return {
            "valid": True,
            "display_name": f"{normalized}, {country}",
            "normalized_name": normalized,
            "osm_id": "",
            "latitude": 0,
            "longitude": 0,
            "importance": 0,
            "postal_code": "",
            "fallback": True
        }
    except Exception as e:
        print(f"Geocoding error: {e}")
        # En cas d'erreur, normaliser quand même
        normalized = city.strip().title()
        return {
            "valid": True,
            "display_name": f"{normalized}, {country}",
            "normalized_name": normalized,
            "osm_id": "",
            "latitude": 0,
            "longitude": 0,
            "importance": 0,
            "postal_code": "",
            "fallback": True
        }


async def autocomplete_cities(query: str, country: Optional[str] = None, limit: int = 5) -> list:
    """
    Autocomplétion de villes pour améliorer l'UX.
    
    Args:
        query: Début du nom de ville
        country: Pays pour filtrer (optionnel)
        limit: Nombre de résultats max
        
    Returns:
        Liste de suggestions de villes
    """
    if not query.strip() or len(query) < 2:
        return []
    
    search_query = f"{query}, {country}" if country else query
    
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(
                NOMINATIM_URL,
                headers=NOMINATIM_HEADERS,
                params={
                    "q": search_query,
                    "format": "json",
                    "limit": limit,
                    "addressdetails": 1
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                suggestions = []
                
                for result in data:
                    place_type = result.get("type", "")
                    if any(t in place_type for t in ["city", "town", "village", "municipality"]):
                        suggestions.append({
                            "name": result.get("name", ""),
                            "display_name": result.get("display_name", ""),
                            "importance": float(result.get("importance", 0))
                        })
                
                return suggestions
                
    except Exception as e:
        print(f"Autocomplete error: {e}")
        return []
    
    return []

