#!/usr/bin/env python3
"""
Quick script to train YOLOv12 for 1 epoch
"""
from pathlib import Path
from ultralytics import YOLO
import torch
import logging
import shutil

# Setup
project_root = Path(__file__).parent
dataset_yaml = project_root / 'data' / 'processed' / 'dataset.yaml'
models_dir = project_root / 'models'
models_dir.mkdir(exist_ok=True)

print("=" * 60)
print("TRAINING YOLOV12 (1 EPOCH)")
print("=" * 60)

# Apply PyTorch patch
_ORIGINAL_TORCH_LOAD = torch.load
def _patched_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return _ORIGINAL_TORCH_LOAD(*args, **kwargs)
torch.load = _patched_load

# Suppress logs
logging.getLogger("ultralytics").setLevel(logging.ERROR)

# Try to load YOLOv11/v12/v9
models_to_try = ['yolo11n.pt', 'yolov11n.pt', 'yolo12n.pt', 'yolov12n.pt', 'yolo9n.pt']
model = None
model_name = None

print("\nLoading YOLO model...")
for m in models_to_try:
    try:
        model = YOLO(m)
        model_name = m
        print(f"✓ Loaded {m}")
        break
    except:
        continue

if model is None:
    print("✗ No YOLO model available")
    print("  Try: pip install --upgrade ultralytics")
    exit(1)

# Train
print(f"\nDataset: {dataset_yaml}")
print("Starting training (1 epoch)...")

results = model.train(
    data=str(dataset_yaml),
    epochs=1,
    imgsz=640,
    device='mps',
    verbose=False,
    name='yolov12_dental',
    save=True,
    plots=True
)

# Save model
latest_run_dir = Path(results.save_dir)
source_weights = latest_run_dir / 'weights' / 'best.pt'
dest_weights = models_dir / 'yolov12_best.pt'

if source_weights.exists():
    shutil.copy(source_weights, dest_weights)
    size_mb = dest_weights.stat().st_size / (1024*1024)
    print(f"\n✓ Model saved: {dest_weights} ({size_mb:.1f} MB)")
else:
    print(f"\n✗ ERROR: Training failed")
    exit(1)

print("\n" + "=" * 60)
print("TRAINING COMPLETE!")
print("=" * 60)
print("\nYou can now run: python test_pipeline.py")
print("The Gradio app will show both models for comparison.")
