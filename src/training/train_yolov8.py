import argparse
import os
from pathlib import Path
from ultralytics import YOLO


def main():
    parser = argparse.ArgumentParser(description="Train YOLOv8 on a dataset.yaml")
    parser.add_argument("data", help="Path to dataset.yaml")
    parser.add_argument("--model", default="yolov8n.pt", help="Base model (e.g., yolov8n.pt, yolov8s.pt)")
    parser.add_argument("--epochs", type=int, default=20, help="Number of training epochs")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    args = parser.parse_args()

    runs_dir = Path("runs")
    runs_dir.mkdir(exist_ok=True)
    model = YOLO(args.model)
    results = model.train(data=args.data, epochs=args.epochs, imgsz=args.imgsz, project=str(runs_dir), name="yolov8_local")

    best = Path(results.save_dir) / "weights" / "best.pt"
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    dest = models_dir / "yolov8_best.pt"
    if best.exists():
        import shutil
        shutil.copy2(best, dest)
        print(f"Saved best weights to: {dest}")
    else:
        print("Training finished but best.pt not found. Check runs directory.")


if __name__ == "__main__":
    main()
