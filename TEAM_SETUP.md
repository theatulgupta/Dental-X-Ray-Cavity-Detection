# Team Setup Guide

## Quick Start (5 Minutes)

### Option 1: Conda (Recommended for ML Projects)

```bash
# 1. Install Miniconda/Anaconda
# 2. Clone and setup
git clone https://github.com/theatulgupta/Dental-X-Ray-Cavity-Detection.git
cd Dental-X-Ray-Cavity-Detection

# 3. Create conda environment
conda env create -f environment.yml
conda activate dental-xray

# 4. Clone YOLOv12 (required for YOLOv12 training - not in main repo)
git clone https://github.com/THU-MIG/yolov10.git yolov12
cd yolov12
pip install -e .
cd ..

# 5. Run
python app.py              # Gradio at http://localhost:7860
jupyter notebook           # Jupyter notebooks
```

### Option 2: Docker

```bash
# 1. Install Docker Desktop from https://www.docker.com/products/docker-desktop
# 2. Clone and run
cd Dental-X-Ray-Cavity-Detection
make app        # Gradio at http://localhost:7860
make jupyter    # Jupyter at http://localhost:8888
```

```bash
# To train YOLOv8, open Jupyter (make jupyter) and run notebooks/02_train_yolov8.ipynb

### Option 3: Python venv (Fallback)

```bash
# 1. Install Python 3.11+
# 2. Setup environment
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Clone YOLOv12 (required for YOLOv12 training - not in main repo)
git clone https://github.com/THU-MIG/yolov10.git yolov12
cd yolov12
pip install -e .
cd ..

# 5. Run
python app.py
jupyter notebook
```

---

## Why Conda for ML?

**Problem:** Deep learning needs PyTorch, CUDA, specific versions → conflicts everywhere

**Solution:** Conda = best package manager for ML/AI projects

✅ Better dependency resolution (PyTorch, CUDA, MKL)  
✅ Handles both Python and system packages  
✅ Cross-platform (Windows/Mac/Linux)  
✅ Industry standard for data science  
✅ Easy environment sharing with `environment.yml`

---

## Daily Workflow

### With Conda (Recommended)

```bash
git pull
conda activate dental-xray

# Run app
python app.py

# Run notebooks
jupyter notebook

# Deactivate when done
conda deactivate
```

### With Docker

```bash
git pull
make app          # Run Gradio app
make jupyter      # Run Jupyter notebooks
make train-v12    # Train YOLOv12
# To train YOLOv8, open Jupyter (make jupyter) and run notebooks/02_train_yolov8.ipynb
make down         # Stop containers
make build        # Rebuild (only if requirements.txt changed)
```

### With Python venv

```bash
git pull
source .venv/bin/activate
pip install -r requirements.txt  # Only if changed
python app.py
jupyter notebook
```

---

## Project Structure

```plaintext
notebooks/
  01_prepare_dataset.ipynb    # Process local dataset (data/raw/)
  02_train_yolov8.ipynb        # Train YOLOv8
  03_train_yolov12.ipynb       # Train YOLOv12
  04_compare_metrics.ipynb     # Compare models

src/app/
  app.py                        # Gradio interface
  inference.py                  # Model loading & prediction

models/
  yolov8_best.pt               # Trained YOLOv8 weights
  yolov12_best.pt              # Trained YOLOv12 weights
  yolov8_metrics.json          # YOLOv8 performance metrics
  yolov12_metrics.json         # YOLOv12 performance metrics

data/
  raw/                          # Your local dataset (64 images)
    images/                     # Original X-ray images
    object_detection_labels/    # YOLO format labels (.txt)
  processed/                    # Train/val/test splits (auto-generated)
    dataset.yaml                # Dataset configuration
    train/images/, train/labels/
    val/images/, val/labels/
    test/images/, test/labels/

yolov12/                      # YOLOv12 repo (clone separately - not in git)
                              # Clone with: git clone https://github.com/THU-MIG/yolov10.git yolov12

environment.yml               # Conda environment specification
requirements.txt              # Pip requirements
```

**Note:** The `yolov12/` directory is NOT included in the repository. You must clone it separately as shown in the setup instructions above.

---

## Training Models

### Step 1: Prepare Dataset

```bash
# Open and run 01_prepare_dataset.ipynb
# This will:
# - Find all images in data/raw/images/
# - Match with labels in data/raw/object_detection_labels/
# - Split into train (70%), val (15%), test (15%)
# - Copy to data/processed/ with proper YOLO structure
# - Create dataset.yaml configuration file
```

### Step 2: Quick Training (1 epoch for testing)

```bash
# Conda
conda activate dental-xray
jupyter notebook  # Open 02_train_yolov8.ipynb or 03_train_yolov12.ipynb

# Docker
# Open `02_train_yolov8.ipynb` inside Jupyter (use `make jupyter`) to run YOLOv8 training
make train-v12
```

### Step 3: Full Training (50-100 epochs for production)

- Open `02_train_yolov8.ipynb`, change `epochs=50` (or 100), run all cells
- Open `03_train_yolov12.ipynb`, change `epochs=50` (or 100), run all cells
- Open `04_compare_metrics.ipynb`, run to see which model is better

**Training Tips:**

- 8GB RAM: Use `epochs=50`, `batch=8`
- 24GB+ RAM: Use `epochs=100`, `batch=16` or higher
- Mac M1/M2/M3: YOLOv8 uses MPS, YOLOv12 uses CPU
- Training time: ~20s per epoch (YOLOv8), ~varies (YOLOv12 on CPU)

---

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
# Fix conflicts
git add .
git rebase --continue
git push
```

---

## Troubleshooting

### Docker Issues

**Port already in use**

```bash
# Edit docker-compose.yml, change:
ports: ["7861:7860"]  # Use different port
```

**Code changes not showing**

- Files are mounted, no rebuild needed
- Just refresh browser

**Can't install new package**

```bash
# 1. Add to requirements.txt
# 2. Rebuild
make build
```

**Docker daemon not running**

- Start Docker Desktop app

### Manual Setup Issues

**Wrong Python version**

```bash
python --version  # Should be 3.13.5
# Install correct version or use Docker
```

**Import errors**

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**PyTorch weights_only error**

- Already patched in notebooks
- If error persists, check notebook cell 1

---

## What to Commit to Git

✅ Commit:

- Code (`src/`, `notebooks/`)
- Config (`requirements.txt`, `Dockerfile`)
- Docs (`README.md`)

❌ Don't Commit:

- `.venv/` (virtual environment)
- `runs/` (training outputs - too large)
- `*.pt` (model weights - use Git LFS or separate storage)
- Dataset images (use Git LFS or cloud storage)

---

## Complete Commands Reference

### Docker Commands

```bash
make help         # Show all commands
make build        # Build Docker image
make app          # Run Gradio (http://localhost:7860)
make jupyter      # Run Jupyter (http://localhost:8888)
make up           # Run both app and jupyter
make down         # Stop all containers
make train-v12    # Train YOLOv12
make clean        # Remove all containers and images
./test_docker.sh  # Test Docker setup
```
```bash
# To train YOLOv8, open Jupyter (make jupyter) and run notebooks/02_train_yolov8.ipynb
# Docker commands for other tasks:
make build        # Build Docker image
make app          # Run Gradio (http://localhost:7860)
make jupyter      # Run Jupyter (http://localhost:8888)
make up           # Run both app and jupyter
make down         # Stop all containers
make train-v12    # Train YOLOv12
make clean        # Remove all containers and images
./test_docker.sh  # Test Docker setup
```

### Manual Commands

```bash
# Activate environment
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows

# Run app
python app.py                    # Gradio app
jupyter notebook                 # Jupyter

# Train
python -m src.training.train_yolov12
# To train YOLOv8, open notebooks/02_train_yolov8.ipynb inside Jupyter
```

---

## File Structure Explained

```
Dockerfile              # Docker image definition (Python 3.13.5 + deps)
docker-compose.yml      # Services: app + jupyter
Makefile               # Shortcuts (make app, make jupyter)
requirements.txt       # Python packages with versions
.gitignore            # Don't commit large files
test_docker.sh        # Test if Docker works

notebooks/            # 4 notebooks for training workflow
src/                  # Source code
models/               # Trained .pt files
data/                 # Dataset
runs/                 # Training outputs (auto-generated)
```

---

## Environment Details

**Python:** 3.11+  
**PyTorch:** 2.0.0+ (with MPS for Mac M1/M2/M3)  
**Ultralytics:** 8.2.0 (YOLO framework)  
**Gradio:** 5.0.0 (web UI)  
**Dataset:** 64 local images, 4 cavity classes (cavity_class_0 to cavity_class_3)  
**Train/Val/Test Split:** 70% / 15% / 15% (~45/10/10 images)

**Package Manager:**

- Conda (recommended): `environment.yml`
- Pip (alternative): `requirements.txt`

---

## Next Steps After Setup

1. **Test setup**

   ```bash
   # Conda
   conda activate dental-xray
   python app.py  # Should open Gradio at http://localhost:7860

   # Docker
   ./test_docker.sh  # or: make app
   ```

2. **Prepare dataset**

   - Open `01_prepare_dataset.ipynb`
   - Run all cells to process local data from `data/raw/`
   - Verify output: `data/processed/dataset.yaml` created

3. **Train models**

   - Open `02_train_yolov8.ipynb`, run all cells
   - Open `03_train_yolov12.ipynb`, run all cells
   - Models saved to `models/yolov8_best.pt` and `models/yolov12_best.pt`

4. **Compare models**

   - Open `04_compare_metrics.ipynb`, run all cells
   - See which model performs better on your local dataset

5. **Deploy**
   - Best model weights are in `models/` directory
   - Use `app.py` for Gradio interface
   - Deploy to Hugging Face Spaces or cloud if needed

---

## Support

**Docker not working?**

- Check if Docker Desktop is running
- Run `./test_docker.sh` for diagnostics
- Try `make down` then `make build` then `make app`

**Manual setup issues?**

- Verify Python 3.13.5: `python --version`
- Activate venv: `source .venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

**Training errors?**

- Check dataset exists in `data/raw/dental/`
- Run `01_prepare_dataset.ipynb` first
- PyTorch patch is in all training notebooks

**Still stuck?**

- Check README.md for more details
- Ask team lead
