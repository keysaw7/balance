"""
BALANCE Data Service
Service de gestion des données pour la plateforme BALANCE
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import os

app = FastAPI(
    title="BALANCE Data Service",
    description="Service de gestion des données pour BALANCE",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

class DataSource(BaseModel):
    """Modèle pour une source de données"""
    id: str
    name: str
    type: str
    description: str
    last_updated: str
    size: int

class DataQuery(BaseModel):
    """Modèle pour une requête de données"""
    domain: str
    region: str
    filters: Dict[str, Any]

@app.get("/")
async def root():
    """Point d'entrée principal du service de données"""
    return {
        "message": "BALANCE Data Service",
        "version": "0.1.0",
        "status": "running",
        "capabilities": [
            "Gestion des données publiques",
            "Anonymisation et confidentialité",
            "Agrégation et analyse",
            "Export et visualisation"
        ]
    }

@app.get("/health")
async def health_check():
    """Vérification de santé du service de données"""
    return {"status": "healthy", "service": "data-service"}

@app.get("/sources", response_model=List[DataSource])
async def get_data_sources():
    """Retourne la liste des sources de données disponibles"""
    sources = [
        DataSource(
            id="insee_1",
            name="Données INSEE - Population",
            type="statistiques",
            description="Données démographiques françaises",
            last_updated="2024-01-15",
            size=1024000
        ),
        DataSource(
            id="eurostat_1",
            name="Eurostat - Indicateurs sociaux",
            type="statistiques",
            description="Indicateurs sociaux européens",
            last_updated="2024-01-10",
            size=2048000
        ),
        DataSource(
            id="open_data_1",
            name="Open Data France - Transports",
            type="données_ouvertes",
            description="Données de transport public français",
            last_updated="2024-01-20",
            size=512000
        )
    ]
    return sources

@app.post("/query")
async def query_data(query: DataQuery):
    """
    Exécute une requête sur les données
    
    Args:
        query: Paramètres de la requête
        
    Returns:
        Résultats de la requête
    """
    # Simulation de requête (à remplacer par la vraie logique)
    return {
        "query_id": "query_123",
        "results": [
            {"indicator": "population", "value": 67000000, "year": 2023},
            {"indicator": "pib_par_habitant", "value": 42000, "year": 2023},
            {"indicator": "taux_chomage", "value": 7.4, "year": 2023}
        ],
        "metadata": {
            "total_records": 3,
            "query_time": "0.045s",
            "sources": ["insee_1", "eurostat_1"]
        }
    }

@app.get("/domains")
async def get_available_domains():
    """Retourne les domaines de données disponibles"""
    return {
        "domains": [
            "démographie",
            "économie",
            "santé",
            "éducation",
            "environnement",
            "transport",
            "logement"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=True
    )
