#!/bin/bash

# BALANCE - Script d'initialisation
# Ce script configure l'environnement de développement initial

set -e

echo "🚀 Initialisation de BALANCE..."

# Couleurs pour les logs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier les prérequis
check_prerequisites() {
    log_info "Vérification des prérequis..."
    
    # Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
    
    # Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
    
    # Node.js (optionnel pour le développement local)
    if ! command -v node &> /dev/null; then
        log_warn "Node.js n'est pas installé. L'interface web sera disponible via Docker."
    fi
    
    # Python (optionnel pour le développement local)
    if ! command -v python3 &> /dev/null; then
        log_warn "Python 3 n'est pas installé. Le backend sera disponible via Docker."
    fi
    
    log_info "Prérequis vérifiés ✓"
}

# Créer les répertoires nécessaires
create_directories() {
    log_info "Création des répertoires..."
    
    # Répertoires de données
    mkdir -p data/raw data/processed data/curated
    touch data/raw/.gitkeep data/processed/.gitkeep data/curated/.gitkeep
    
    # Répertoires de logs
    mkdir -p logs
    
    # Répertoires de configuration
    mkdir -p config/secrets config/ssl
    
    # Répertoires de modèles
    mkdir -p models/zeus models/cache
    
    # Répertoires de tests
    mkdir -p test-data test-results
    
    log_info "Répertoires créés ✓"
}

# Créer les fichiers de configuration par défaut
create_config_files() {
    log_info "Création des fichiers de configuration..."
    
    # Configuration de base
    cat > config/config.yaml << EOF
# Configuration de BALANCE
app:
  name: "BALANCE"
  version: "0.1.0"
  environment: "development"

database:
  host: "postgres"
  port: 5432
  name: "balance"
  user: "balance"
  password: "balance_dev"

redis:
  host: "redis"
  port: 6379
  db: 0

zeus:
  model_path: "/models"
  max_workers: 4
  timeout: 300

api:
  host: "0.0.0.0"
  port: 8000
  cors_origins: ["http://localhost:3000"]

web:
  host: "0.0.0.0"
  port: 3000
  api_url: "http://localhost:8000"

monitoring:
  prometheus_port: 9090
  grafana_port: 3001
EOF

    # Configuration de développement
    cat > config/development.yaml << EOF
# Configuration de développement
debug: true
log_level: "DEBUG"
reload: true

database:
  echo: true

zeus:
  debug: true
  log_requests: true
EOF

    # Configuration de production
    cat > config/production.yaml << EOF
# Configuration de production
debug: false
log_level: "INFO"
reload: false

database:
  echo: false
  pool_size: 20
  max_overflow: 30

zeus:
  debug: false
  log_requests: false
  cache_size: 1000
EOF

    log_info "Fichiers de configuration créés ✓"
}

# Créer les fichiers d'environnement
create_env_files() {
    log_info "Création des fichiers d'environnement..."
    
    # Fichier .env pour le développement
    cat > .env << EOF
# Environnement de développement BALANCE
NODE_ENV=development
DEBUG=true

# Base de données
DATABASE_URL=postgresql://balance:balance_dev@localhost:5432/balance
POSTGRES_DB=balance
POSTGRES_USER=balance
POSTGRES_PASSWORD=balance_dev

# Redis
REDIS_URL=redis://localhost:6379

# API
API_HOST=0.0.0.0
API_PORT=8000

# Web
WEB_HOST=0.0.0.0
WEB_PORT=3000
NEXT_PUBLIC_API_URL=http://localhost:8000

# Zeus
ZEUS_API_URL=http://localhost:8001
ZEUS_MODEL_PATH=/models

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001

# Sécurité (à changer en production)
JWT_SECRET=your-secret-key-change-in-production
ENCRYPTION_KEY=your-encryption-key-change-in-production
EOF

    # Fichier .env.example
    cp .env .env.example
    
    log_info "Fichiers d'environnement créés ✓"
}

# Installer les dépendances Python (si Python est disponible)
install_python_deps() {
    if command -v python3 &> /dev/null; then
        log_info "Installation des dépendances Python..."
        
        # Créer un environnement virtuel
        python3 -m venv venv
        source venv/bin/activate
        
        # Installer les dépendances
        pip install --upgrade pip
        pip install -r requirements.txt
        
        log_info "Dépendances Python installées ✓"
    else
        log_warn "Python 3 non disponible, les dépendances seront installées via Docker"
    fi
}

# Installer les dépendances Node.js (si Node.js est disponible)
install_node_deps() {
    if command -v node &> /dev/null; then
        log_info "Installation des dépendances Node.js..."
        
        # Installer les dépendances du frontend
        if [ -d "apps/web" ]; then
            cd apps/web
            npm install
            cd ../..
        fi
        
        # Installer les dépendances du mobile
        if [ -d "apps/mobile" ]; then
            cd apps/mobile
            npm install
            cd ../..
        fi
        
        log_info "Dépendances Node.js installées ✓"
    else
        log_warn "Node.js non disponible, les dépendances seront installées via Docker"
    fi
}

# Créer les fichiers de base pour chaque service
create_service_files() {
    log_info "Création des fichiers de base des services..."
    
    # API Gateway
    mkdir -p apps/api
    cat > apps/api/requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
redis==5.0.1
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
httpx==0.25.2
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
flake8==6.1.0
EOF

    # Zeus
    mkdir -p backend/zeus
    cat > backend/zeus/requirements.txt << EOF
torch==2.1.1
transformers==4.35.2
numpy==1.24.3
pandas==2.1.3
scikit-learn==1.3.2
optuna==3.4.0
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
redis==5.0.1
httpx==0.25.2
pytest==7.4.3
black==23.11.0
flake8==6.1.0
EOF

    # Service de données
    mkdir -p backend/data
    cat > backend/data/requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
redis==5.0.1
pandas==2.1.3
numpy==1.24.3
pydantic==2.5.0
httpx==0.25.2
pytest==7.4.3
black==23.11.0
flake8==6.1.0
EOF

    # Service de gouvernance
    mkdir -p backend/governance
    cat > backend/governance/requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
redis==5.0.1
pydantic==2.5.0
httpx==0.25.2
pytest==7.4.3
black==23.11.0
flake8==6.1.0
EOF

    log_info "Fichiers de base des services créés ✓"
}

# Créer les Dockerfiles de base
create_dockerfiles() {
    log_info "Création des Dockerfiles..."
    
    # API Gateway Dockerfile
    cat > apps/api/Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

    # Zeus Dockerfile
    cat > backend/zeus/Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système pour PyTorch
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["python", "-m", "zeus.main", "--host", "0.0.0.0", "--port", "8001"]
EOF

    # Service de données Dockerfile
    cat > backend/data/Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["python", "-m", "data.main", "--host", "0.0.0.0", "--port", "8002"]
EOF

    # Service de gouvernance Dockerfile
    cat > backend/governance/Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8003

CMD ["python", "-m", "governance.main", "--host", "0.0.0.0", "--port", "8003"]
EOF

    # Interface web Dockerfile
    cat > apps/web/Dockerfile << EOF
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
EOF

    log_info "Dockerfiles créés ✓"
}

# Créer les fichiers de configuration de monitoring
create_monitoring_config() {
    log_info "Création de la configuration de monitoring..."
    
    # Prometheus configuration
    cat > infrastructure/monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

scrape_configs:
  - job_name: 'balance-api'
    static_configs:
      - targets: ['api-gateway:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'balance-zeus'
    static_configs:
      - targets: ['zeus:8001']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'balance-data'
    static_configs:
      - targets: ['data-service:8002']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'balance-governance'
    static_configs:
      - targets: ['governance-service:8003']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
EOF

    # Grafana configuration
    mkdir -p infrastructure/monitoring/grafana/provisioning/datasources
    cat > infrastructure/monitoring/grafana/provisioning/datasources/prometheus.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF

    log_info "Configuration de monitoring créée ✓"
}

# Créer les scripts utilitaires
create_utility_scripts() {
    log_info "Création des scripts utilitaires..."
    
    # Script de vérification de santé
    cat > scripts/setup/health-check.sh << 'EOF'
#!/bin/bash

# Script de vérification de santé des services BALANCE

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Vérifier les services
check_service() {
    local service=$1
    local url=$2
    local name=$3
    
    if curl -s -f "$url" > /dev/null 2>&1; then
        log_info "$name est en ligne ✓"
        return 0
    else
        log_error "$name n'est pas accessible à $url"
        return 1
    fi
}

log_info "Vérification de la santé des services BALANCE..."

# Vérifier l'API Gateway
check_service "api-gateway" "http://localhost:8000/health" "API Gateway"

# Vérifier Zeus
check_service "zeus" "http://localhost:8001/health" "Zeus"

# Vérifier le service de données
check_service "data-service" "http://localhost:8002/health" "Service de données"

# Vérifier le service de gouvernance
check_service "governance-service" "http://localhost:8003/health" "Service de gouvernance"

# Vérifier l'interface web
check_service "web-app" "http://localhost:3000" "Interface web"

# Vérifier Prometheus
check_service "prometheus" "http://localhost:9090" "Prometheus"

# Vérifier Grafana
check_service "grafana" "http://localhost:3001" "Grafana"

log_info "Vérification terminée!"
EOF

    chmod +x scripts/setup/health-check.sh

    log_info "Scripts utilitaires créés ✓"
}

# Fonction principale
main() {
    log_info "Démarrage de l'initialisation de BALANCE..."
    
    check_prerequisites
    create_directories
    create_config_files
    create_env_files
    create_service_files
    create_dockerfiles
    create_monitoring_config
    create_utility_scripts
    
    # Installer les dépendances si les outils sont disponibles
    install_python_deps
    install_node_deps
    
    log_info "🎉 Initialisation de BALANCE terminée avec succès!"
    log_info ""
    log_info "Prochaines étapes:"
    log_info "1. Exécuter 'make dev' pour démarrer l'environnement de développement"
    log_info "2. Exécuter 'make health' pour vérifier que tous les services fonctionnent"
    log_info "3. Consulter la documentation dans docs/"
    log_info ""
    log_info "Services disponibles:"
    log_info "  - Interface web: http://localhost:3000"
    log_info "  - API: http://localhost:8000"
    log_info "  - Documentation: http://localhost:8000/docs"
    log_info "  - Monitoring: http://localhost:9090"
    log_info ""
    log_info "Bonne contribution à BALANCE! 🚀"
}

# Exécuter le script principal
main "$@"
