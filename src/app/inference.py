
import os
import torch
from typing import List, Tuple
import numpy as np
from ultralytics import YOLO

# This must run ONCE when the module is first imported
_ORIGINAL_TORCH_LOAD = torch.load 

# Patched torch.load to use weights_only=False for Ultralytics models -> Don't support
def _patched_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return _ORIGINAL_TORCH_LOAD(*args, **kwargs)

torch.load = _patched_load

# Loading trained YOLO model from .pt file
def load_model(model_path: str) -> YOLO:
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return YOLO(model_path)


    # Run prediction on an image array and return annotated image (RGB) and boxes.
    


def predict(model: YOLO, image: np.ndarray, conf: float = 0.25, iou: float = 0.45) -> Tuple[np.ndarray, List[List[float]]]:
        
    # Args:
      # model: YOLO model instance
      # image: Input image as numpy array
      # conf: Confidence threshold
      # iou: IoU threshold for NMS
    results = model.predict(image, conf=conf, iou=iou, verbose=False)
    
    # Returns -> Tuple of (annotated_image_rgb, list_of_boxes)
    result = results[0]
    
    # Plot with custom visualization settings (red boxes, labels, confidence)
    annotated_bgr = result.plot(
        conf=True,          # Show confidence scores
        labels=True,        # Show class labels
        boxes=True,         # Show bounding boxes
        line_width=2,       # Box thickness
    )
    
    # Convert BGR to RGB for Gradio
    annotated_rgb = annotated_bgr[:, :, ::-1]
    
    # Extract bounding boxes
    boxes = result.boxes.xyxy.cpu().numpy().tolist() if result.boxes is not None else []
    
    return annotated_rgb, boxes
