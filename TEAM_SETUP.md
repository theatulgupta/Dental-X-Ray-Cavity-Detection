# Team Setup Guide

This project uses a single Conda environment for everything (no Docker, no venv). Follow the steps below to get running fast.

## Quick Start (5 minutes)

```bash
# 1) Install Miniconda (https://docs.conda.io/en/latest/miniconda.html)

# 2) Clone repo
git clone https://github.com/theatulgupta/Dental-X-Ray-Cavity-Detection.git
cd Dental-X-Ray-Cavity-Detection

# 3) Create and activate environment
conda env create -f environment.yml
conda activate dental-xray

# 4) (One-time) Clone YOLOv12 locally for training
#    Note: yolov12 is not part of this repo; keep it sibling to notebooks/src
git clone https://github.com/THU-MIG/yolov10.git yolov12
cd yolov12 && pip install -e . && cd ..

# 5) Run
python app.py            # Gradio app at http://localhost:7860
jupyter notebook         # Open notebooks
```

## Why Conda

- Reproducible: environment.yml pins compatible versions
- ML-friendly: handles Python + system packages (MKL, PyTorch, etc.)
- Cross-platform: works on macOS, Linux, Windows
- One source of truth: no Docker or venv complexity

## Daily Workflow

```bash
git pull
conda activate dental-xray

# Run app
python app.py

# Work in notebooks
jupyter notebook

# When done
conda deactivate
```

## Project Structure

```plaintext
notebooks/
   01_prepare_dataset.ipynb     # Prepare local dataset and splits
   02_train_yolov8.ipynb        # Train YOLOv8
   03_train_yolov12.ipynb       # Train YOLOv12 (uses local yolov12 repo)
   04_compare_metrics.ipynb     # Compare metrics and resources

src/app/
   app.py                       # Gradio UI
   inference.py                 # Model loading & prediction helpers

models/
   yolov8_best.pt               # Best YOLOv8 weights (optional, not committed)
   yolov12_best.pt              # Best YOLOv12 weights (optional, not committed)
   yolov8_metrics.json          # Metrics (optional)
   yolov12_metrics.json         # Metrics (optional)

data/
   raw/                         # Your local dataset
      images/                    # Original X-ray images
      object_detection_labels/   # YOLO format labels (.txt)
   processed/
      dataset.yaml               # Auto-generated
      train/{images,labels}
      val/{images,labels}
      test/{images,labels}

yolov12/                       # Local clone for YOLOv12 (not part of repo)

environment.yml                # Conda environment spec
requirements.txt               # Optional pip mirror of dependencies
```

Note: The `yolov12/` folder is not tracked by git. Clone it locally as shown above.

## Train Models

### 1) Prepare dataset

Open and run `notebooks/01_prepare_dataset.ipynb`:

- Scans `data/raw/images/` and `data/raw/object_detection_labels/`
- Splits into train/val/test
- Writes `data/processed/dataset.yaml`

### 2) Quick test training (1 epoch)

```bash
conda activate dental-xray
jupyter notebook  # open 02_train_yolov8.ipynb or 03_train_yolov12.ipynb
```

### 3) Full training (50–100 epochs)

- In `02_train_yolov8.ipynb`, set `epochs=50` (or 100), run all cells
- In `03_train_yolov12.ipynb`, set `epochs=50` (or 100), run all cells
- In `04_compare_metrics.ipynb`, compare and pick the best model

Tips:

- 8GB RAM: `epochs=50`, `batch=8`
- 24GB+ RAM: `epochs=100`, `batch=16`+
- macOS Apple Silicon: YOLOv8 uses MPS; YOLOv12 may use CPU

## Git Workflow

```bash
# Before work
git pull

# After work
git status
git add .
git commit -m "Your message"
git push

# If conflicts
git pull --rebase
# Resolve conflicts
git add .
git rebase --continue
git push
```

## Troubleshooting

### Python version

```bash
python --version  # Expect 3.11.x
```

If different, re-create the environment from `environment.yml`.

### Import errors or missing packages

- Ensure you ran: `conda activate dental-xray`
- If needed: `conda env update -f environment.yml --prune`

### PyTorch weights_only error

- Already patched in notebooks and `src/app/inference.py`
- If it reappears, ensure you’re using our provided environment and latest notebooks

## What to Commit

Commit:

- Code: `src/`, `notebooks/`
- Config: `environment.yml`, `requirements.txt`
- Docs: `README.md`, `TEAM_SETUP.md`

Don’t commit:

- Local environments (`.venv/`, Conda env folders)
- Large outputs (`runs/`), dataset images, or `*.pt` weights (use LFS or cloud)

## Commands Reference (Conda)

```bash
# Activate environment
conda activate dental-xray

# Run app
python app.py  # Gradio at http://localhost:7860

# Notebooks
jupyter notebook

# Optional: training via modules (if provided)
python -m src.training.train_yolov8
python -m src.training.train_yolov12

# Deactivate
conda deactivate
```

## Environment details

See `environment.yml` for exact, tested versions (Python, PyTorch, Ultralytics, Gradio, etc.).

## Next steps

1. Test setup

```bash
conda activate dental-xray
python app.py
```

2. Prepare dataset: run `01_prepare_dataset.ipynb`

3. Train: run `02_train_yolov8.ipynb` and/or `03_train_yolov12.ipynb`

4. Compare models: run `04_compare_metrics.ipynb`

5. Deploy: use `app.py` with the best weights in `models/`
