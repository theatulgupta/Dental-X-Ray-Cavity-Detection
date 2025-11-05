# Dental X-Ray Cavity Detection

Deep learning project to detect cavities in dental X-rays using YOLOv8 and YOLOv12.

---

## 🚀 Quick Start

### Docker (Recommended)

```bash
make app      # Gradio app → http://localhost:7860
make jupyter  # Notebooks → http://localhost:8888
```

### Manual Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux | .venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

📖 **Full setup guide:** [TEAM_SETUP.md](TEAM_SETUP.md)

---

## 📁 Project Structure

```
notebooks/
  01_prepare_dataset.ipynb    # Split data into train/val
  02_train_yolov8.ipynb        # Train YOLOv8 model
  03_train_yolov12.ipynb       # Train YOLOv12 model
  04_compare_metrics.ipynb     # Compare model performance

src/app/
  app.py          # Gradio web interface
  inference.py    # Model loading & prediction

models/
  yolov8_best.pt   # YOLOv8 trained weights
  yolov12_best.pt  # YOLOv12 trained weights

data/
  raw/dental/      # Original dataset
  processed/       # Train/val splits
```

---

## 🎯 Workflow

### 1. Prepare Dataset

```bash
make jupyter
# Open 01_prepare_dataset.ipynb → Run all cells
```

Creates train/val split (80/20) in `data/processed/`

### 2. Train Models

```bash
# Open 02_train_yolov8.ipynb → Change epochs=50 → Run all cells
# Open 03_train_yolov12.ipynb → Change epochs=50 → Run all cells
```

Models saved to `models/yolov8_best.pt` and `models/yolov12_best.pt`

### 3. Compare Models

```bash
# Open 04_compare_metrics.ipynb → Run all cells
```

See performance metrics, training curves, and deployment recommendation.

### 4. Run Gradio App

```bash
make app
# Visit http://localhost:7860
# Upload X-ray → See cavity detections
```

---

## 📊 Key Features

- **Model Comparison:** Side-by-side YOLOv8 vs YOLOv12
- **Bounding Boxes:** Red boxes with class labels and confidence scores
- **Performance Metrics:** mAP, Precision, Recall, Training curves
- **Easy Deployment:** Docker setup for team consistency

---

## 🛠️ Common Commands

```bash
make app          # Run Gradio app
make jupyter      # Run Jupyter notebooks
make train-v8     # Quick YOLOv8 training (1 epoch)
make train-v12    # Quick YOLOv12 training (1 epoch)
make build        # Rebuild Docker image
make down         # Stop containers
```

---

## 🐛 Troubleshooting

**PyTorch weights_only error?**  
Already patched in all notebooks. Just run cells normally.

**No models found?**  
Train models first using notebooks 02 and 03.

**Port already in use?**  
Edit `docker-compose.yml`, change `7860:7860` to `7861:7860`

**More help:** See [TEAM_SETUP.md](TEAM_SETUP.md)

---

## 👥 Team

- ANKIT PAWAR (10, 25MCSA23)
- ATUL KUMAR GUPTA (25MCSS06)
- RICHA VERMA (25MCSS02)
- GOURAV CHOUHAN (25MCSS15)

---

## 📄 License

See [LICENSE](LICENSE) file.

Dataset: <https://www.kaggle.com/datasets/killa92/dental-x-ray-images-dataset>
