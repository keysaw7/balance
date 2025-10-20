"""
BALANCE API Gateway
Point d'entrée principal pour l'API de la plateforme BALANCE
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from routes.ideas import router as ideas_router
from routes.geocoding import router as geocoding_router

app = FastAPI(
    title="BALANCE API",
    description="API Gateway pour la plateforme d'intelligence collective BALANCE",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(ideas_router, prefix="/api")
app.include_router(geocoding_router, prefix="/api")

@app.get("/")
async def root():
    """Point d'entrée principal de l'API"""
    return {
        "message": "BALANCE API Gateway",
        "version": "0.1.0",
        "status": "running",
        "services": {
            "zeus": os.getenv("ZEUS_API_URL", "http://localhost:8001"),
            "data": "http://localhost:8002",
            "governance": "http://localhost:8003"
        }
    }

@app.get("/health")
async def health_check():
    """Vérification de santé de l'API"""
    return {"status": "healthy", "service": "api-gateway"}

@app.get("/api/v1/status")
async def api_status():
    """Statut détaillé de l'API"""
    return {
        "api": "running",
        "version": "0.1.0",
        "environment": os.getenv("NODE_ENV", "development")
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
