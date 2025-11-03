#!/bin/bash
# Deploy to Hugging Face Spaces

set -e

echo "🚀 Deploying to Hugging Face Spaces..."

# Check if HF_TOKEN is set
if [ -z "$HF_TOKEN" ]; then
    echo "Error: HF_TOKEN environment variable is not set"
    echo "Please set it with: export HF_TOKEN=your_token_here"
    exit 1
fi

# Check if HF_SPACE_NAME is set
if [ -z "$HF_SPACE_NAME" ]; then
    echo "Error: HF_SPACE_NAME environment variable is not set"
    echo "Please set it with: export HF_SPACE_NAME=username/space-name"
    exit 1
fi

# Clone or update HF Space
if [ -d "hf_space" ]; then
    echo "Updating existing HF Space..."
    cd hf_space
    git pull
else
    echo "Cloning HF Space..."
    git clone https://huggingface.co/spaces/$HF_SPACE_NAME hf_space
    cd hf_space
fi

# Copy files
echo "Copying files..."
cp ../app.py .
cp -r ../src .
cp -r ../config .
cp ../requirements.txt .

# Create README for HF Space
cat > README.md << 'EOF'
---
title: Dental X-Ray Cavity Detection
emoji: 🦷
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# Dental X-Ray Cavity Detection

AI-powered dental cavity detection using YOLOv8 and YOLOv12 models.

Upload a dental X-ray image to detect and visualize cavities automatically.
EOF

# Commit and push
echo "Committing changes..."
git config user.email "github-actions@github.com"
git config user.name "GitHub Actions"
git add .
git commit -m "Deploy from GitHub Actions - $(date)" || echo "No changes to commit"

echo "Pushing to Hugging Face..."
git push https://user:$HF_TOKEN@huggingface.co/spaces/$HF_SPACE_NAME main

echo "✓ Deployment complete!"
echo "Visit: https://huggingface.co/spaces/$HF_SPACE_NAME"
