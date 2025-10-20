"""
BALANCE Zeus - Modèle d'IA central
Intelligence artificielle pour l'analyse de politiques publiques
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import os

app = FastAPI(
    title="BALANCE Zeus",
    description="Modèle d'IA central pour l'analyse de politiques publiques",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

class PolicyInput(BaseModel):
    """Modèle d'entrée pour l'analyse de politique"""
    domain: str
    region: str
    constraints: Dict[str, Any]
    description: str

class PolicyScenario(BaseModel):
    """Modèle de sortie pour un scénario de politique"""
    id: str
    score: float
    explanation: str
    trade_offs: List[str]
    implementation_cost: float
    timeline: str

@app.get("/")
async def root():
    """Point d'entrée principal de Zeus"""
    return {
        "message": "BALANCE Zeus - Modèle d'IA central",
        "version": "0.1.0",
        "status": "running",
        "capabilities": [
            "Analyse de politiques publiques",
            "Simulation multi-critères",
            "Explication des recommandations",
            "Optimisation Pareto"
        ]
    }

@app.get("/health")
async def health_check():
    """Vérification de santé de Zeus"""
    return {"status": "healthy", "service": "zeus"}

@app.post("/analyze", response_model=List[PolicyScenario])
async def analyze_policy(policy: PolicyInput):
    """
    Analyse une politique publique selon les contraintes données
    
    Args:
        policy: Données de la politique à analyser
        
    Returns:
        Liste des scénarios optimaux avec explications
    """
    # Simulation d'analyse (à remplacer par le vrai modèle)
    scenarios = [
        PolicyScenario(
            id="scenario_1",
            score=0.85,
            explanation="Ce scénario optimise l'efficacité tout en maintenant l'équité sociale",
            trade_offs=["Coût élevé à court terme", "Bénéfices à long terme"],
            implementation_cost=1000000,
            timeline="2-3 ans"
        ),
        PolicyScenario(
            id="scenario_2", 
            score=0.78,
            explanation="Approche progressive avec impact immédiat mais moindre efficacité",
            trade_offs=["Impact limité", "Coût réduit"],
            implementation_cost=500000,
            timeline="1-2 ans"
        )
    ]
    
    return scenarios

@app.get("/domains")
async def get_available_domains():
    """Retourne les domaines d'analyse disponibles"""
    return {
        "domains": [
            "climat",
            "santé",
            "éducation", 
            "mobilité",
            "logement",
            "économie",
            "sécurité"
        ]
    }

@app.get("/regions")
async def get_available_regions():
    """Retourne les régions d'analyse disponibles"""
    return {
        "regions": [
            "france",
            "europe",
            "monde",
            "local"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )
