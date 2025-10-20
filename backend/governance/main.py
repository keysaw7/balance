"""
BALANCE Governance Service
Service de gouvernance démocratique pour la plateforme BALANCE
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import uvicorn
import os

app = FastAPI(
    title="BALANCE Governance Service",
    description="Service de gouvernance démocratique pour BALANCE",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

class Proposal(BaseModel):
    """Modèle pour une proposition de gouvernance"""
    id: str
    title: str
    description: str
    author: str
    created_at: datetime
    status: str
    votes_for: int
    votes_against: int
    technical_review: Optional[str]

class Vote(BaseModel):
    """Modèle pour un vote"""
    proposal_id: str
    voter_id: str
    vote_type: str  # "for", "against", "abstain"
    timestamp: datetime
    justification: Optional[str]

@app.get("/")
async def root():
    """Point d'entrée principal du service de gouvernance"""
    return {
        "message": "BALANCE Governance Service",
        "version": "0.1.0",
        "status": "running",
        "capabilities": [
            "Gestion des propositions",
            "Système de vote démocratique",
            "Référendum technique",
            "Audit et transparence"
        ]
    }

@app.get("/health")
async def health_check():
    """Vérification de santé du service de gouvernance"""
    return {"status": "healthy", "service": "governance-service"}

@app.get("/proposals", response_model=List[Proposal])
async def get_proposals():
    """Retourne la liste des propositions en cours"""
    proposals = [
        Proposal(
            id="prop_001",
            title="Amélioration de l'algorithme d'équité",
            description="Proposition d'amélioration de l'algorithme pour mieux prendre en compte l'équité sociale",
            author="user_123",
            created_at=datetime.now(),
            status="voting",
            votes_for=45,
            votes_against=12,
            technical_review="Analyse technique en cours"
        ),
        Proposal(
            id="prop_002",
            title="Ajout de nouvelles sources de données",
            description="Intégration de nouvelles sources de données européennes",
            author="user_456",
            created_at=datetime.now(),
            status="technical_review",
            votes_for=0,
            votes_against=0,
            technical_review="En attente de validation technique"
        )
    ]
    return proposals

@app.post("/proposals")
async def create_proposal(proposal: Proposal):
    """
    Crée une nouvelle proposition
    
    Args:
        proposal: Données de la proposition
        
    Returns:
        Confirmation de création
    """
    # Simulation de création (à remplacer par la vraie logique)
    return {
        "message": "Proposition créée avec succès",
        "proposal_id": proposal.id,
        "status": "pending_review"
    }

@app.post("/vote")
async def cast_vote(vote: Vote):
    """
    Enregistre un vote sur une proposition
    
    Args:
        vote: Données du vote
        
    Returns:
        Confirmation du vote
    """
    # Simulation de vote (à remplacer par la vraie logique)
    return {
        "message": "Vote enregistré avec succès",
        "vote_id": f"vote_{vote.proposal_id}_{vote.voter_id}",
        "timestamp": vote.timestamp
    }

@app.get("/proposals/{proposal_id}")
async def get_proposal(proposal_id: str):
    """Retourne les détails d'une proposition spécifique"""
    # Simulation de récupération (à remplacer par la vraie logique)
    return {
        "id": proposal_id,
        "title": "Proposition exemple",
        "description": "Description détaillée de la proposition",
        "status": "voting",
        "votes": {
            "for": 45,
            "against": 12,
            "abstain": 3
        },
        "technical_review": "Analyse technique complète disponible"
    }

@app.get("/stats")
async def get_governance_stats():
    """Retourne les statistiques de gouvernance"""
    return {
        "total_proposals": 15,
        "active_proposals": 3,
        "completed_proposals": 12,
        "total_votes": 1250,
        "active_voters": 89,
        "last_activity": "2024-01-20T10:30:00Z"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003,
        reload=True
    )
