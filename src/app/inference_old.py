"""
Inference module for YOLO models
"""
import os
import torch
from typing import List, Tuple
import numpy as np
from ultralytics import YOLO


# Apply PyTorch compatibility patch for PyTorch 2.6+
original_torch_load = torch.load

def patched_torch_load(*args, **kwargs):
    """Patched torch.load to use weights_only=False for Ultralytics models."""
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)

torch.load = patched_torch_load


def load_model(model_path: str) -> YOLO:
    """
    Load a YOLO model from a .pt file.
    
    Args:
        model_path: Path to the .pt model file
        
    Returns:
        Loaded YOLO model
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return YOLO(model_path)


def predict(model: YOLO, image: np.ndarray, conf: float = 0.25, iou: float = 0.45) -> Tuple[np.ndarray, List[List[float]]]:
    """
    Run prediction on an image array and return annotated image (RGB) and boxes.
    
    Args:
        model: YOLO model instance
        image: Input image as numpy array
        conf: Confidence threshold
        iou: IoU threshold for NMS
        
    Returns:
        Tuple of (annotated_image_rgb, list_of_boxes)
    """
    results = model.predict(image, conf=conf, iou=iou, verbose=False)
    result = results[0]
    
    # Ultralytics returns BGR in .plot(); convert to RGB for Gradio
    annotated_bgr = result.plot()
    annotated_rgb = annotated_bgr[:, :, ::-1]
    
    # Extract bounding boxes
    boxes = result.boxes.xyxy.cpu().numpy().tolist() if result.boxes is not None else []
    
    return annotated_rgb, boxes
