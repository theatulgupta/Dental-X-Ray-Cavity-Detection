# Team Setup Guide

## Quick Start (5 Minutes)

### Option 1: Docker (Recommended)

```bash
# 1. Install Docker Desktop from https://www.docker.com/products/docker-desktop
# 2. Clone and run
git clone <your-repo-url>
cd dental-xray-cavity-detection
make app        # Gradio at http://localhost:7860
make jupyter    # Jupyter at http://localhost:8888
```

### Option 2: Manual Setup (Fallback)

```bash
# 1. Install Python 3.13.5
# 2. Setup environment
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python app.py
jupyter notebook
```

---

## Why Docker?

**Problem:** Team members have different Python versions, OS, packages → code breaks

**Solution:** Docker = same environment for everyone, guaranteed

✅ No version conflicts  
✅ Works on Windows/Mac/Linux  
✅ Same setup for dev and deployment  
✅ New members onboard in 5 minutes

---

## Daily Workflow

### With Docker

```bash
git pull
make app          # Run Gradio app
make jupyter      # Run Jupyter notebooks
make train-v8     # Train YOLOv8
make train-v12    # Train YOLOv12
make down         # Stop containers
make build        # Rebuild (only if requirements.txt changed)
```

### Without Docker

```bash
git pull
source .venv/bin/activate
pip install -r requirements.txt  # Only if changed
python app.py
jupyter notebook
```

---

## Project Structure

```
notebooks/
  01_prepare_dataset.ipynb    # Split data (train/val)
  02_train_yolov8.ipynb        # Train YOLOv8
  03_train_yolov12.ipynb       # Train YOLOv12
  04_compare_metrics.ipynb     # Compare models

src/app/
  app.py                        # Gradio interface
  inference.py                  # Model loading & prediction

models/
  yolov8_best.pt               # Trained weights
  yolov12_best.pt

data/
  raw/dental/                   # Original dataset
  processed/                    # Train/val splits
```

---

## Training Models

### Quick Training (1 epoch for testing)

```bash
# Docker
make train-v8
make train-v12

# Manual
python -m src.training.train_yolov8
python -m src.training.train_yolov12
```

### Full Training (in notebooks)

- Open `02_train_yolov8.ipynb`, change `epochs=50`, run all cells
- Open `03_train_yolov12.ipynb`, change `epochs=50`, run all cells
- Open `04_compare_metrics.ipynb`, run to see which model is better

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
make train-v8     # Train YOLOv8
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
python -m src.training.train_yolov8
python -m src.training.train_yolov12
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

**Python:** 3.13.5  
**PyTorch:** 2.5.1 (with MPS for Mac M1)  
**Ultralytics:** 8.2.0 (YOLO framework)  
**Gradio:** 5.0.0 (web UI)  
**Dataset:** 86 images, 4 cavity classes (0-3)

---

## Next Steps After Setup

1. **Test setup**

   ```bash
   ./test_docker.sh  # or manually run python app.py
   ```

2. **Train models**

   - Open `02_train_yolov8.ipynb`, run all cells
   - Open `03_train_yolov12.ipynb`, run all cells

3. **Compare models**

   - Open `04_compare_metrics.ipynb`, run all cells
   - See which model performs better

4. **Deploy**
   - Best model is in `models/` directory
   - Use `app.py` for Gradio interface
   - Deploy to Hugging Face Spaces if needed

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
