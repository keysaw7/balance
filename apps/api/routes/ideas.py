from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
import hashlib

from database import get_db, Idea, init_db
from services.openai_service import normalize_idea_with_ai
from services.embeddings_service import find_similar_ideas

router = APIRouter(prefix="/ideas", tags=["ideas"])

# Initialiser la DB au démarrage
init_db()


class IdeaCreate(BaseModel):
    text: str
    country: str
    city: str


class IdeaResponse(BaseModel):
    id: str
    text: str
    normalized: str
    count: int
    country: str
    city: str
    createdAt: str


async def generate_idea_id(text: str, country: str, city: str, normalized: str) -> str:
    """Génère un ID unique basé sur le contenu normalisé"""
    content = f"{normalized}_{country}_{city}"
    return hashlib.md5(content.encode()).hexdigest()[:12]


@router.post("", response_model=IdeaResponse)
async def create_idea(idea: IdeaCreate, db: Session = Depends(get_db)):
    """
    Soumettre une nouvelle idée.
    L'idée est normalisée avec OpenAI et fusionnée si elle existe déjà.
    Utilise les embeddings pour une détection sémantique avancée.
    """
    # 1. Normalisation avec OpenAI gpt-4o-mini (multilingue)
    normalized = await normalize_idea_with_ai(idea.text)
    idea_id = await generate_idea_id(idea.text, idea.country, idea.city, normalized)
    
    # 2. Chercher si l'idée existe déjà (même normalisation + même lieu)
    existing = db.query(Idea).filter(
        Idea.normalized == normalized,
        Idea.country == idea.country,
        Idea.city == idea.city
    ).first()
    
    # 3. Si pas trouvé par normalisation, essayer avec embeddings (détection sémantique)
    if not existing:
        all_ideas_same_location = db.query(Idea).filter(
            Idea.country == idea.country,
            Idea.city == idea.city
        ).all()
        
        if all_ideas_same_location:
            existing_list = [(i.id, i.normalized) for i in all_ideas_same_location]
            similar = await find_similar_ideas(normalized, existing_list, threshold=0.88)
            
            if similar:
                similar_id, similarity_score = similar
                existing = db.query(Idea).filter(Idea.id == similar_id).first()
                print(f"🔍 Idée similaire détectée par embeddings: {similarity_score:.3f}")
    
    # 4. Incrémenter ou créer
    
    if existing:
        # Incrémenter le compteur
        existing.count += 1
        existing.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        
        return IdeaResponse(
            id=existing.id,
            text=existing.text,
            normalized=existing.normalized,
            count=existing.count,
            country=existing.country,
            city=existing.city,
            createdAt=existing.created_at.isoformat()
        )
    
    # Créer nouvelle idée
    new_idea = Idea(
        id=idea_id,
        text=idea.text,
        normalized=normalized,
        count=1,
        country=idea.country,
        city=idea.city
    )
    
    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)
    
    return IdeaResponse(
        id=new_idea.id,
        text=new_idea.text,
        normalized=new_idea.normalized,
        count=new_idea.count,
        country=new_idea.country,
        city=new_idea.city,
        createdAt=new_idea.created_at.isoformat()
    )


@router.get("", response_model=List[IdeaResponse])
async def get_ideas(
    country: Optional[str] = None, 
    city: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Récupérer les idées pour un lieu donné.
    """
    query = db.query(Idea)
    
    if country:
        query = query.filter(Idea.country == country)
    if city:
        query = query.filter(Idea.city == city)
    
    ideas = query.all()
    
    return [
        IdeaResponse(
            id=idea.id,
            text=idea.text,
            normalized=idea.normalized,
            count=idea.count,
            country=idea.country,
            city=idea.city,
            createdAt=idea.created_at.isoformat()
        )
        for idea in ideas
    ]


@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Statistiques globales.
    """
    all_ideas = db.query(Idea).all()
    
    return {
        'total_ideas': len(all_ideas),
        'total_contributions': sum(idea.count for idea in all_ideas),
        'countries': len(set(idea.country for idea in all_ideas)),
        'cities': len(set(f"{idea.country}_{idea.city}" for idea in all_ideas)),
    }

