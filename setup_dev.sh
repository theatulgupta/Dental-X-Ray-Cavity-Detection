#!/bin/bash
# Setup script for local development environment

set -e

echo "🚀 Setting up Dental X-Ray Cavity Detection Development Environment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
REQUIRED_PYTHON="3.10"
echo -e "${YELLOW}Checking Python version...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo "Found Python $PYTHON_VERSION"
else
    echo "Python 3 is not installed. Please install Python $REQUIRED_PYTHON"
    exit 1
fi

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Install development dependencies
echo -e "${YELLOW}Installing development dependencies...${NC}"
pip install \
    jupyter \
    ipykernel \
    black \
    flake8 \
    mypy \
    pytest \
    pytest-cov \
    pre-commit

# Setup pre-commit hooks
echo -e "${YELLOW}Setting up pre-commit hooks...${NC}"
if [ -f ".pre-commit-config.yaml" ]; then
    pre-commit install
    echo -e "${GREEN}✓ Pre-commit hooks installed${NC}"
fi

# Create necessary directories
echo -e "${YELLOW}Creating project directories...${NC}"
mkdir -p data/raw/dental/images
mkdir -p data/processed
mkdir -p data/annotations
mkdir -p models
mkdir -p results/training_logs
mkdir -p results/metrics
mkdir -p tests

# Create empty __init__.py files
touch tests/__init__.py
touch src/__init__.py

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Setup completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To deactivate, run:"
echo "  deactivate"
echo ""
echo "To run the app:"
echo "  python app.py"
echo ""
