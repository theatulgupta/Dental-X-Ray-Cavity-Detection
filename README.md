# Dental X-Ray Cavity Detection

Deep learning project comparing YOLOv8 and YOLOv12 for cavity detection using local dental X-ray dataset.

**Dataset:** 64 local X-ray images with YOLO format annotations  
**Classes:** 4 cavity types (cavity_class_0 to cavity_class_3)  
**Models:** YOLOv8n vs YOLOv12n

---

## 🚀 Quick Start

### Docker

```bash
make app      # Gradio app → http://localhost:7860
make jupyter  # Notebooks → http://localhost:8888
```

### Local Setup

#### Option 1: Conda (Recommended)

```bash
# 1. Create environment
conda env create -f environment.yml
conda activate dental-xray

# 2. Clone YOLOv12 repository (required for YOLOv12 training)
git clone https://github.com/THU-MIG/yolov10.git yolov12
cd yolov12
pip install -e .
cd ..

# 3. Run the app
python app.py
```

#### Option 2: Python venv

```bash
# 1. Create environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Clone YOLOv12 repository (required for YOLOv12 training)
git clone https://github.com/THU-MIG/yolov10.git yolov12
cd yolov12
pip install -e .
cd ..

# 3. Run the app
python app.py
```

---

## 📁 Structure

```plaintext
notebooks/
  01_prepare_dataset.ipynb     # Process local dataset (data/raw/)
  02_train_yolov8.ipynb        # Train YOLOv8n
  03_train_yolov12.ipynb       # Train YOLOv12n
  04_compare_metrics.ipynb     # Compare models

data/
  raw/
    images/                    # 64 X-ray images
    object_detection_labels/   # YOLO format labels
  processed/
    dataset.yaml               # Generated dataset config
    train/images/, train/labels/
    val/images/, val/labels/
    test/images/, test/labels/

models/
  yolov8_best.pt              # Trained YOLOv8 weights
  yolov12_best.pt             # Trained YOLOv12 weights
  yolov8_metrics.json         # Performance metrics
  yolov12_metrics.json

environment.yml               # Conda environment
requirements.txt              # Pip requirements
app.py                        # Gradio interface
```

---

## 🎯 Workflow

### 1. Prepare Dataset

```bash
# Run 01_prepare_dataset.ipynb
# - Finds images in data/raw/images/
# - Matches with labels in data/raw/object_detection_labels/
# - Splits into train (70%), val (15%), test (15%)
# - Creates data/processed/ with YOLO structure
# - Generates dataset.yaml
```

### 2. Train Models

```bash
# Run 02_train_yolov8.ipynb (YOLOv8n, configurable epochs)
# Run 03_train_yolov12.ipynb (YOLOv12n, configurable epochs)
# Models and metrics saved to models/

# Training tips:
# - 8GB RAM: epochs=50, batch=8
# - 24GB+ RAM: epochs=100, batch=16+
# - Default: epochs=1 (for quick testing)
```

### 3. Compare Results

```bash
# Run 04_compare_metrics.ipynb
# View comparison charts:
# - Training time
# - Model parameters
# - Inference speed
# - mAP50, mAP50-95
# - Get recommendation for best model
```

### 4. Deploy

```bash
conda activate dental-xray  # or: source .venv/bin/activate
python app.py
# Open http://localhost:7860
# Upload dental X-rays for detection
```

---

## 📊 Features

- **Local Dataset Processing**: Custom dental X-ray images with YOLO annotations
- **Dual Model Comparison**: YOLOv8n vs YOLOv12n side-by-side
- **Comprehensive Metrics**: Training time, params, speed, mAP50, mAP50-95
- **Interactive UI**: Gradio web interface for real-time detection
- **Conda Support**: Easy environment setup with `environment.yml`
- **Docker Ready**: Consistent deployment across platforms
- **Automated Splitting**: 70/15/15 train/val/test split
- **MPS Acceleration**: Mac M1/M2/M3 GPU support (YOLOv8)

---

## 🛠️ Commands

```bash
make app          # Run Gradio app
make jupyter      # Run notebooks
make build        # Rebuild Docker image
make down         # Stop containers
```

---

## 📄 License

See [LICENSE](LICENSE) file.

**Dataset:** Roboflow - deep-learning-nesrt/dental-xray-cavity-8x2vh
