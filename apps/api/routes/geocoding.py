"""
Routes pour la géolocalisation et validation de villes
"""
from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional, List

from services.geocoding_service import validate_city, autocomplete_cities

router = APIRouter(prefix="/geocoding", tags=["geocoding"])


class CityValidationResponse(BaseModel):
    valid: bool
    display_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    importance: Optional[float] = None
    fallback: Optional[bool] = False
    error: Optional[str] = None


class CitySuggestion(BaseModel):
    name: str
    display_name: str
    importance: float


@router.get("/validate", response_model=CityValidationResponse)
async def validate_city_endpoint(
    city: str = Query(..., description="Nom de la ville"),
    country: str = Query(..., description="Nom du pays")
):
    """
    Valide qu'une ville existe dans un pays donné.
    Utilise l'API Nominatim (OpenStreetMap) - gratuite et sans clé API.
    """
    result = await validate_city(city, country)
    return CityValidationResponse(**result)


@router.get("/autocomplete", response_model=List[CitySuggestion])
async def autocomplete_cities_endpoint(
    query: str = Query(..., min_length=2, description="Début du nom de ville"),
    country: Optional[str] = Query(None, description="Pays pour filtrer"),
    limit: int = Query(5, ge=1, le=10, description="Nombre de suggestions max")
):
    """
    Autocomplétion de villes pour améliorer l'UX.
    """
    suggestions = await autocomplete_cities(query, country, limit)
    return [CitySuggestion(**s) for s in suggestions]

