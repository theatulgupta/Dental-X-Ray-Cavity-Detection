.PHONY: help setup install install-dev clean test lint format docker-build docker-up docker-down train-yolov8 train-yolov12 run-app

# Variables
PYTHON := python3
PIP := pip
VENV := venv
DOCKER_COMPOSE := docker-compose
PROJECT_NAME := dental-xray-detection

# Colors for terminal output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

##@ General

help: ## Display this help message
	@echo "$(BLUE)Dental X-Ray Cavity Detection - Makefile Commands$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make $(GREEN)<target>$(NC)\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development Setup

setup: ## Initial project setup (creates venv, installs deps)
	@echo "$(YELLOW)🚀 Setting up development environment...$(NC)"
	@chmod +x setup_dev.sh
	@./setup_dev.sh
	@echo "$(GREEN)✓ Setup complete!$(NC)"

install: ## Install production dependencies
	@echo "$(YELLOW)📦 Installing production dependencies...$(NC)"
	@$(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed!$(NC)"

install-dev: install ## Install development dependencies
	@echo "$(YELLOW)📦 Installing development dependencies...$(NC)"
	@$(PIP) install -r requirements-dev.txt
	@pre-commit install
	@echo "$(GREEN)✓ Dev dependencies installed!$(NC)"

clean: ## Clean up cache, logs, and temporary files
	@echo "$(YELLOW)🧹 Cleaning up...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@rm -rf htmlcov/ .coverage coverage.xml
	@echo "$(GREEN)✓ Cleanup complete!$(NC)"

##@ Code Quality

lint: ## Run all linters (flake8, mypy, black check)
	@echo "$(YELLOW)🔍 Running linters...$(NC)"
	@black --check src/ tests/ || true
	@flake8 src/ tests/ --max-line-length=120 --extend-ignore=E203,W503 || true
	@isort --check-only --profile black src/ tests/ || true
	@mypy src/ --ignore-missing-imports || true
	@echo "$(GREEN)✓ Linting complete!$(NC)"

format: ## Auto-format code with black and isort
	@echo "$(YELLOW)✨ Formatting code...$(NC)"
	@black src/ tests/
	@isort --profile black src/ tests/
	@echo "$(GREEN)✓ Code formatted!$(NC)"

test: ## Run unit tests with coverage
	@echo "$(YELLOW)🧪 Running tests...$(NC)"
	@pytest tests/ -v --cov=src --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Tests complete! Coverage report: htmlcov/index.html$(NC)"

test-quick: ## Run tests without coverage
	@echo "$(YELLOW)🧪 Running quick tests...$(NC)"
	@pytest tests/ -v
	@echo "$(GREEN)✓ Tests complete!$(NC)"

##@ Docker Operations

docker-build: ## Build all Docker images
	@echo "$(YELLOW)🐳 Building Docker images...$(NC)"
	@$(DOCKER_COMPOSE) build
	@echo "$(GREEN)✓ Docker images built!$(NC)"

docker-build-prod: ## Build production image only
	@echo "$(YELLOW)🐳 Building production image...$(NC)"
	@docker build --target production -t $(PROJECT_NAME):prod .
	@echo "$(GREEN)✓ Production image built!$(NC)"

docker-up: ## Start all Docker containers
	@echo "$(YELLOW)🐳 Starting Docker containers...$(NC)"
	@$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)✓ Containers started!$(NC)"
	@$(DOCKER_COMPOSE) ps

docker-up-dev: ## Start development container with Jupyter
	@echo "$(YELLOW)🐳 Starting development container...$(NC)"
	@$(DOCKER_COMPOSE) up -d dev
	@echo "$(GREEN)✓ Dev container started!$(NC)"
	@echo "$(BLUE)Jupyter Lab: http://localhost:8888$(NC)"
	@echo "$(BLUE)Gradio App: http://localhost:7860$(NC)"

docker-up-app: ## Start production app container
	@echo "$(YELLOW)🐳 Starting app container...$(NC)"
	@$(DOCKER_COMPOSE) up -d app
	@echo "$(GREEN)✓ App container started!$(NC)"
	@echo "$(BLUE)Gradio App: http://localhost:7860$(NC)"

docker-down: ## Stop all Docker containers
	@echo "$(YELLOW)🐳 Stopping Docker containers...$(NC)"
	@$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✓ Containers stopped!$(NC)"

docker-logs: ## View Docker container logs
	@$(DOCKER_COMPOSE) logs -f

docker-shell-dev: ## Open shell in development container
	@$(DOCKER_COMPOSE) exec dev bash

docker-shell-app: ## Open shell in app container
	@$(DOCKER_COMPOSE) exec app bash

docker-clean: ## Remove all containers, images, and volumes
	@echo "$(YELLOW)🐳 Cleaning Docker resources...$(NC)"
	@$(DOCKER_COMPOSE) down -v --rmi all
	@echo "$(GREEN)✓ Docker cleanup complete!$(NC)"

##@ Training

train-yolov8: ## Train YOLOv8 model
	@echo "$(YELLOW)🔥 Training YOLOv8...$(NC)"
	@$(PYTHON) -m src.training.train_yolov8
	@echo "$(GREEN)✓ Training complete!$(NC)"

train-yolov12: ## Train YOLOv12 model
	@echo "$(YELLOW)🔥 Training YOLOv12...$(NC)"
	@$(PYTHON) -m src.training.train_yolov12
	@echo "$(GREEN)✓ Training complete!$(NC)"

train-docker: ## Train models using Docker (GPU)
	@echo "$(YELLOW)🔥 Training with Docker...$(NC)"
	@$(DOCKER_COMPOSE) run --rm train
	@echo "$(GREEN)✓ Training complete!$(NC)"

##@ Application

run-app: ## Run Gradio app locally
	@echo "$(YELLOW)🚀 Starting Gradio app...$(NC)"
	@$(PYTHON) app.py
	@echo "$(GREEN)✓ App running at http://localhost:7860$(NC)"

run-jupyter: ## Run Jupyter Lab
	@echo "$(YELLOW)📊 Starting Jupyter Lab...$(NC)"
	@jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

##@ Data Processing

prepare-data: ## Prepare and split dataset
	@echo "$(YELLOW)📊 Preparing dataset...$(NC)"
	@$(PYTHON) -m src.data_prep.convert_to_yolo_format
	@$(PYTHON) -m src.data_prep.split_dataset
	@echo "$(GREEN)✓ Data preparation complete!$(NC)"

##@ Evaluation

compare-models: ## Compare YOLOv8 vs YOLOv12 performance
	@echo "$(YELLOW)📊 Comparing models...$(NC)"
	@$(PYTHON) -m src.evaluation.compare_models
	@echo "$(GREEN)✓ Comparison complete!$(NC)"

inference-benchmark: ## Run inference benchmarks
	@echo "$(YELLOW)⚡ Running inference benchmark...$(NC)"
	@$(PYTHON) -m src.evaluation.inference_benchmark
	@echo "$(GREEN)✓ Benchmark complete!$(NC)"

##@ Git & CI/CD

git-status: ## Show git status and branch info
	@echo "$(BLUE)Git Status:$(NC)"
	@git status -s
	@echo ""
	@echo "$(BLUE)Current Branch:$(NC) $(shell git branch --show-current)"
	@echo "$(BLUE)Last Commit:$(NC) $(shell git log -1 --oneline)"

pre-commit: ## Run pre-commit hooks manually
	@echo "$(YELLOW)🔧 Running pre-commit hooks...$(NC)"
	@pre-commit run --all-files
	@echo "$(GREEN)✓ Pre-commit checks complete!$(NC)"

##@ Monitoring

monitor-gpu: ## Monitor GPU usage
	@watch -n 1 nvidia-smi

monitor-docker: ## Monitor Docker container resources
	@docker stats

##@ Deployment

deploy-hf: ## Deploy to Hugging Face Spaces (requires HF_TOKEN)
	@echo "$(YELLOW)🚀 Deploying to Hugging Face Spaces...$(NC)"
	@bash scripts/deploy_to_hf.sh
	@echo "$(GREEN)✓ Deployment complete!$(NC)"

##@ Utilities

check-env: ## Check environment setup
	@echo "$(BLUE)Environment Check:$(NC)"
	@echo "Python version: $(shell $(PYTHON) --version)"
	@echo "Pip version: $(shell $(PIP) --version)"
	@echo "Docker version: $(shell docker --version 2>/dev/null || echo 'Not installed')"
	@echo "Docker Compose version: $(shell $(DOCKER_COMPOSE) --version 2>/dev/null || echo 'Not installed')"
	@echo "CUDA available: $(shell $(PYTHON) -c 'import torch; print(torch.cuda.is_available())' 2>/dev/null || echo 'PyTorch not installed')"
