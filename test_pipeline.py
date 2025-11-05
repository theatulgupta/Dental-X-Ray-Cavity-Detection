#!/usr/bin/env python3
"""
Quick test script to verify the entire pipeline works
Runs 1 epoch of training and launches Gradio app
"""

print("=" * 60)
print("DENTAL X-RAY CAVITY DETECTION - PIPELINE TEST")
print("=" * 60)

# Step 1: Check if model exists
import os
from pathlib import Path

project_root = Path(__file__).parent
model_path = project_root / 'models' / 'yolov8_best.pt'

if model_path.exists():
    print(f"\n✓ Found existing model: {model_path}")
    print(f"  Size: {model_path.stat().st_size / (1024*1024):.1f} MB")
    use_existing = input("\nUse existing model? (y/n): ").lower().strip()
    
    if use_existing == 'n':
        train_model = True
    else:
        train_model = False
else:
    print(f"\n✗ No existing model found at {model_path}")
    print("  Will train a new model (1 epoch for testing)")
    train_model = True

# Step 2: Train model if needed
if train_model:
    print("\n" + "=" * 60)
    print("STEP 1: TRAINING YOLOV8 (1 EPOCH)")
    print("=" * 60)
    
    from ultralytics import YOLO
    import torch
    
    # Apply PyTorch patch
    _ORIGINAL_TORCH_LOAD = torch.load
    def _patched_load(*args, **kwargs):
        if 'weights_only' not in kwargs:
            kwargs['weights_only'] = False
        return _ORIGINAL_TORCH_LOAD(*args, **kwargs)
    torch.load = _patched_load
    
    # Suppress logs
    import logging
    logging.getLogger("ultralytics").setLevel(logging.ERROR)
    
    # Load model and train
    dataset_yaml = project_root / 'data' / 'processed' / 'dataset.yaml'
    
    if not dataset_yaml.exists():
        print(f"\n✗ ERROR: Dataset not found at {dataset_yaml}")
        print("  Please run notebook 01_prepare_dataset.ipynb first")
        exit(1)
    
    print(f"\nDataset: {dataset_yaml}")
    print("Loading YOLOv8n...")
    model = YOLO('yolov8n.pt')
    
    print("\nStarting training (1 epoch)...")
    results = model.train(
        data=str(dataset_yaml),
        epochs=1,
        imgsz=640,
        device='mps',
        verbose=False,
        name='yolov8_dental',
        save=True,
        plots=True
    )
    
    # Save model
    import shutil
    latest_run_dir = Path(results.save_dir)
    source_weights = latest_run_dir / 'weights' / 'best.pt'
    
    if source_weights.exists():
        models_dir = project_root / 'models'
        models_dir.mkdir(exist_ok=True)
        shutil.copy(source_weights, model_path)
        print(f"\n✓ Model saved: {model_path}")
    else:
        print(f"\n✗ ERROR: Training failed - no weights found")
        exit(1)

# Step 3: Launch Gradio app
print("\n" + "=" * 60)
print("STEP 2: LAUNCHING GRADIO APP")
print("=" * 60)

import sys
sys.path.insert(0, str(project_root))

from src.app.app import iface

print("\n🚀 Starting Gradio interface...")
print("   The app will open in your browser automatically")
print("   Press Ctrl+C to stop the server\n")

iface.launch(share=False)
