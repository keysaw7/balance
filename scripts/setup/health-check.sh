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
