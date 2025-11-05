#!/bin/bash

echo "🔍 Testing Docker setup..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop first."
    exit 1
fi

echo "✅ Docker is installed"

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running. Please start Docker Desktop."
    exit 1
fi

echo "✅ Docker daemon is running"

# Build the image
echo ""
echo "🔨 Building Docker image..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi

# Test the app container
echo ""
echo "🧪 Testing app container..."
docker-compose run --rm dental-app python -c "import torch; import ultralytics; print(f'PyTorch: {torch.__version__}'); print(f'Ultralytics: {ultralytics.__version__}')"

if [ $? -eq 0 ]; then
    echo "✅ App container works"
else
    echo "❌ App container failed"
    exit 1
fi

echo ""
echo "✅ All tests passed! Your Docker setup is ready."
echo ""
echo "Next steps:"
echo "  make app      - Run Gradio app"
echo "  make jupyter  - Run Jupyter notebooks"
