#!/bin/bash
# Next Steps Execution Script
# This script performs all the next steps automatically

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}  Dental X-Ray Detection Setup${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""

# Step 1: Create virtual environment
echo -e "${YELLOW}Step 1/6: Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi
echo ""

# Step 2: Activate and upgrade pip
echo -e "${YELLOW}Step 2/6: Activating environment and upgrading pip...${NC}"
source venv/bin/activate
pip install --upgrade pip setuptools wheel --quiet
echo -e "${GREEN}✓ Pip upgraded${NC}"
echo ""

# Step 3: Install dependencies
echo -e "${YELLOW}Step 3/6: Installing dependencies...${NC}"
echo "This may take a few minutes..."
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓ Production dependencies installed${NC}"
echo ""

# Step 4: Install development dependencies
echo -e "${YELLOW}Step 4/6: Installing development dependencies...${NC}"
pip install -r requirements-dev.txt --quiet
echo -e "${GREEN}✓ Development dependencies installed${NC}"
echo ""

# Step 5: Setup pre-commit hooks
echo -e "${YELLOW}Step 5/6: Installing pre-commit hooks...${NC}"
pre-commit install
echo -e "${GREEN}✓ Pre-commit hooks installed${NC}"
echo ""

# Step 6: Create necessary directories
echo -e "${YELLOW}Step 6/6: Creating project directories...${NC}"
mkdir -p data/raw/dental/images
mkdir -p data/processed/{train,val,test}/{images,labels}
mkdir -p data/annotations
mkdir -p models
mkdir -p results/training_logs
mkdir -p results/metrics
touch tests/__init__.py
touch src/__init__.py
echo -e "${GREEN}✓ Directories created${NC}"
echo ""

# Environment check
echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}  Environment Check${NC}"
echo -e "${BLUE}=====================================${NC}"
echo -e "Python version: ${GREEN}$(python --version)${NC}"
echo -e "Pip version: ${GREEN}$(pip --version | cut -d' ' -f1-2)${NC}"
echo -e "Virtual env: ${GREEN}venv${NC}"
echo ""

# Show installed key packages
echo -e "${BLUE}Key packages installed:${NC}"
pip list | grep -E "torch|ultralytics|gradio|pytest|black" || echo "Checking packages..."
echo ""

echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}  ✓ Setup Complete!${NC}"
echo -e "${GREEN}=====================================${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "1. Activate the environment: ${BLUE}source venv/bin/activate${NC}"
echo -e "2. Run tests: ${BLUE}make test${NC}"
echo -e "3. Start the app: ${BLUE}make run-app${NC}"
echo -e "4. See all commands: ${BLUE}make help${NC}"
echo ""
echo -e "${YELLOW}For Docker:${NC}"
echo -e "1. Build images: ${BLUE}make docker-build${NC}"
echo -e "2. Start app: ${BLUE}make docker-up-app${NC}"
echo ""
