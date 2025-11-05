import argparse
import glob
import json
import os
import time
from pathlib import Path

from ultralytics import YOLO


def count_parameters(model: YOLO) -> int:
    return sum(p.numel() for p in model.model.parameters())


def benchmark(model_path: str, images_dir: str, warmup: int = 1) -> dict:
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")
    model = YOLO(model_path)

    image_paths = sorted(
        [p for ext in ("*.png", "*.jpg", "*.jpeg", "*.bmp") for p in glob.glob(os.path.join(images_dir, ext))]
    )
    if not image_paths:
        raise FileNotFoundError(f"No images found in {images_dir}")

    # Warmup
    for _ in range(max(0, warmup)):
        model.predict(image_paths[0], verbose=False)

    times = []
    for p in image_paths:
        start = time.perf_counter()
        model.predict(p, verbose=False)
        times.append(time.perf_counter() - start)

    report = {
        "model_path": model_path,
        "num_images": len(image_paths),
        "avg_inference_time_s": sum(times) / len(times),
        "params": count_parameters(model)
    }
    return report


def main():
    parser = argparse.ArgumentParser(description="Benchmark YOLO model inference time")
    parser.add_argument("model", help="Path to model .pt file")
    parser.add_argument("images", help="Directory of images to run inference on")
    parser.add_argument("--out", default="results/metrics/benchmark.json", help="Output JSON path")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    rep = benchmark(args.model, args.images)
    with open(args.out, "w") as f:
        json.dump(rep, f, indent=2)
    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main()
