#!/bin/bash
# Quick start script for team members

set -e

echo "🦷 Dental X-Ray Cavity Detection - Quick Start"
echo "================================================"
echo ""

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "✓ Docker is installed"
    DOCKER_AVAILABLE=true
else
    echo "✗ Docker is not installed"
    DOCKER_AVAILABLE=false
fi

# Ask user preference
echo ""
echo "Choose your development environment:"
echo "1) Local (Python venv) - Recommended for development"
echo "2) Docker - Recommended for consistency"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "Setting up local development environment..."
        chmod +x setup_dev.sh
        ./setup_dev.sh
        echo ""
        echo "✓ Setup complete!"
        echo ""
        echo "Next steps:"
        echo "  1. Activate venv: source venv/bin/activate"
        echo "  2. Run app: python app.py"
        echo "  3. Or use: make run-app"
        ;;
    2)
        if [ "$DOCKER_AVAILABLE" = false ]; then
            echo "Error: Docker is not installed. Please install Docker first."
            exit 1
        fi
        echo ""
        echo "Setting up Docker environment..."
        docker-compose build
        echo ""
        echo "✓ Docker images built!"
        echo ""
        echo "Next steps:"
        echo "  1. Start app: docker-compose up -d app"
        echo "  2. Or use: make docker-up-app"
        echo "  3. Access at: http://localhost:7860"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "For more commands, run: make help"
