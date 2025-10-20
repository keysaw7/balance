# BALANCE - Makefile

.PHONY: help setup dev build test clean deploy docs

# Variables
DOCKER_COMPOSE = docker-compose
PYTHON = python3
NODE = node
NPM = npm

# Couleurs pour les logs
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Afficher cette aide
	@echo "$(GREEN)BALANCE - Commandes disponibles:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

setup: ## Configuration initiale du projet
	@echo "$(GREEN)Configuration de BALANCE...$(NC)"
	@./scripts/setup/init.sh
	@echo "$(GREEN)Configuration terminée!$(NC)"

dev: ## Démarrer l'environnement de développement
	@echo "$(GREEN)Démarrage de l'environnement de développement...$(NC)"
	@$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)Services démarrés!$(NC)"
	@echo "  - Interface web: http://localhost:3000"
	@echo "  - API: http://localhost:8000"
	@echo "  - Documentation: http://localhost:8000/docs"
	@echo "  - Monitoring: http://localhost:9090"

build: ## Construire toutes les images Docker
	@echo "$(GREEN)Construction des images Docker...$(NC)"
	@$(DOCKER_COMPOSE) build
	@echo "$(GREEN)Images construites!$(NC)"

test: ## Exécuter tous les tests
	@echo "$(GREEN)Exécution des tests...$(NC)"
	@$(DOCKER_COMPOSE) exec api-gateway python -m pytest tests/unit/
	@$(DOCKER_COMPOSE) exec api-gateway python -m pytest tests/integration/
	@$(DOCKER_COMPOSE) exec web-app npm test
	@echo "$(GREEN)Tests terminés!$(NC)"

test-unit: ## Exécuter les tests unitaires
	@echo "$(GREEN)Tests unitaires...$(NC)"
	@$(DOCKER_COMPOSE) exec api-gateway python -m pytest tests/unit/ -v

test-integration: ## Exécuter les tests d'intégration
	@echo "$(GREEN)Tests d'intégration...$(NC)"
	@$(DOCKER_COMPOSE) exec api-gateway python -m pytest tests/integration/ -v

test-e2e: ## Exécuter les tests end-to-end
	@echo "$(GREEN)Tests end-to-end...$(NC)"
	@$(DOCKER_COMPOSE) exec web-app npm run test:e2e

test-security: ## Exécuter les tests de sécurité
	@echo "$(GREEN)Tests de sécurité...$(NC)"
	@$(DOCKER_COMPOSE) exec api-gateway python -m pytest tests/security/ -v

lint: ## Vérifier le code avec les linters
	@echo "$(GREEN)Vérification du code...$(NC)"
	@$(DOCKER_COMPOSE) exec api-gateway python -m black --check .
	@$(DOCKER_COMPOSE) exec api-gateway python -m flake8 .
	@$(DOCKER_COMPOSE) exec web-app npm run lint
	@echo "$(GREEN)Vérification terminée!$(NC)"

format: ## Formater le code
	@echo "$(GREEN)Formatage du code...$(NC)"
	@$(DOCKER_COMPOSE) exec api-gateway python -m black .
	@$(DOCKER_COMPOSE) exec web-app npm run format
	@echo "$(GREEN)Formatage terminé!$(NC)"

logs: ## Afficher les logs de tous les services
	@$(DOCKER_COMPOSE) logs -f

logs-api: ## Afficher les logs de l'API
	@$(DOCKER_COMPOSE) logs -f api-gateway

logs-zeus: ## Afficher les logs de Zeus
	@$(DOCKER_COMPOSE) logs -f zeus

logs-web: ## Afficher les logs de l'interface web
	@$(DOCKER_COMPOSE) logs -f web-app

shell-api: ## Ouvrir un shell dans le conteneur API
	@$(DOCKER_COMPOSE) exec api-gateway /bin/bash

shell-zeus: ## Ouvrir un shell dans le conteneur Zeus
	@$(DOCKER_COMPOSE) exec zeus /bin/bash

shell-web: ## Ouvrir un shell dans le conteneur web
	@$(DOCKER_COMPOSE) exec web-app /bin/sh

db-migrate: ## Exécuter les migrations de base de données
	@echo "$(GREEN)Migration de la base de données...$(NC)"
	@$(DOCKER_COMPOSE) exec api-gateway python -m alembic upgrade head
	@echo "$(GREEN)Migration terminée!$(NC)"

db-reset: ## Réinitialiser la base de données
	@echo "$(RED)ATTENTION: Cette action va supprimer toutes les données!$(NC)"
	@read -p "Êtes-vous sûr? (y/N): " confirm && [ "$$confirm" = "y" ]
	@$(DOCKER_COMPOSE) down -v
	@$(DOCKER_COMPOSE) up -d postgres
	@$(DOCKER_COMPOSE) exec api-gateway python -m alembic upgrade head
	@echo "$(GREEN)Base de données réinitialisée!$(NC)"

data-load: ## Charger des données de test
	@echo "$(GREEN)Chargement des données de test...$(NC)"
	@$(DOCKER_COMPOSE) exec data-service python -m data.scripts.load_sample_data
	@echo "$(GREEN)Données chargées!$(NC)"

zeus-train: ## Entraîner le modèle Zeus
	@echo "$(GREEN)Entraînement du modèle Zeus...$(NC)"
	@$(DOCKER_COMPOSE) exec zeus python -m zeus.training.train
	@echo "$(GREEN)Entraînement terminé!$(NC)"

zeus-evaluate: ## Évaluer les performances de Zeus
	@echo "$(GREEN)Évaluation de Zeus...$(NC)"
	@$(DOCKER_COMPOSE) exec zeus python -m zeus.evaluation.evaluate
	@echo "$(GREEN)Évaluation terminée!$(NC)"

docs: ## Générer la documentation
	@echo "$(GREEN)Génération de la documentation...$(NC)"
	@$(DOCKER_COMPOSE) exec api-gateway python -m sphinx-build -b html docs/ docs/_build/html
	@echo "$(GREEN)Documentation générée dans docs/_build/html/$(NC)"

docs-serve: ## Servir la documentation localement
	@echo "$(GREEN)Documentation disponible sur http://localhost:8080$(NC)"
	@cd docs/_build/html && python -m http.server 8080

clean: ## Nettoyer les conteneurs et volumes
	@echo "$(GREEN)Nettoyage...$(NC)"
	@$(DOCKER_COMPOSE) down -v --remove-orphans
	@docker system prune -f
	@echo "$(GREEN)Nettoyage terminé!$(NC)"

clean-all: ## Nettoyer complètement (images, volumes, cache)
	@echo "$(RED)ATTENTION: Cette action va supprimer toutes les images et volumes!$(NC)"
	@read -p "Êtes-vous sûr? (y/N): " confirm && [ "$$confirm" = "y" ]
	@$(DOCKER_COMPOSE) down -v --remove-orphans
	@docker system prune -af
	@docker volume prune -f
	@echo "$(GREEN)Nettoyage complet terminé!$(NC)"

deploy-staging: ## Déployer en environnement de staging
	@echo "$(GREEN)Déploiement en staging...$(NC)"
	@./scripts/deployment/deploy-staging.sh
	@echo "$(GREEN)Déploiement terminé!$(NC)"

deploy-prod: ## Déployer en production
	@echo "$(RED)ATTENTION: Déploiement en production!$(NC)"
	@read -p "Êtes-vous sûr? (y/N): " confirm && [ "$$confirm" = "y" ]
	@./scripts/deployment/deploy-prod.sh
	@echo "$(GREEN)Déploiement en production terminé!$(NC)"

health: ## Vérifier la santé des services
	@echo "$(GREEN)Vérification de la santé des services...$(NC)"
	@./scripts/setup/health-check.sh
	@echo "$(GREEN)Vérification terminée!$(NC)"

backup: ## Sauvegarder les données
	@echo "$(GREEN)Sauvegarde des données...$(NC)"
	@./scripts/backup/backup.sh
	@echo "$(GREEN)Sauvegarde terminée!$(NC)"

restore: ## Restaurer les données
	@echo "$(RED)ATTENTION: Cette action va restaurer les données!$(NC)"
	@read -p "Êtes-vous sûr? (y/N): " confirm && [ "$$confirm" = "y" ]
	@./scripts/backup/restore.sh
	@echo "$(GREEN)Restauration terminée!$(NC)"

# Commandes de développement rapide
dev-quick: ## Démarrage rapide (sans monitoring)
	@$(DOCKER_COMPOSE) up -d postgres redis api-gateway zeus web-app

dev-full: ## Démarrage complet avec monitoring
	@$(DOCKER_COMPOSE) up -d

stop: ## Arrêter tous les services
	@$(DOCKER_COMPOSE) down

restart: ## Redémarrer tous les services
	@$(DOCKER_COMPOSE) restart

status: ## Afficher le statut des services
	@$(DOCKER_COMPOSE) ps
