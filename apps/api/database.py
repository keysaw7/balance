"""
Configuration de la base de données PostgreSQL
"""
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://balance:balance@postgres:5432/balance"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Idea(Base):
    """Modèle de données pour une idée citoyenne"""
    __tablename__ = "ideas"

    id = Column(String, primary_key=True, index=True)
    text = Column(String, nullable=False)
    normalized = Column(String, nullable=False, index=True)
    count = Column(Integer, default=1)
    country = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def get_db():
    """Dependency pour obtenir une session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialiser la base de données (créer les tables)"""
    Base.metadata.create_all(bind=engine)

