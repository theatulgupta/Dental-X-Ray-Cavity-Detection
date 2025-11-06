# Dental X-Ray Cavity Detection

Deep learning project comparing YOLOv8 and YOLOv12 for cavity detection using Roboflow dataset.

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
conda env create -f environment.yml
conda activate dental-xray
python app.py
```

#### Option 2: Python venv

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

---

## 📁 Structure

```plaintext
notebooks/
  01_prepare_dataset.ipynb     # Download Roboflow dataset
  02_train_yolov8.ipynb        # Train YOLOv8n
  03_train_yolov12.ipynb       # Train YOLOv12n
  04_compare_metrics.ipynb     # Compare models

models/
  yolov8_best.pt              # Trained weights
  yolov12_best.pt
  yolov8_metrics.json         # Performance metrics
  yolov12_metrics.json

app.py                        # Gradio interface
```

---

## 🎯 Workflow

### 1. Prepare Dataset

```bash
# Run 01_prepare_dataset.ipynb
# Downloads from Roboflow and saves to data/processed/
```

### 2. Train Models

```bash
# Run 02_train_yolov8.ipynb (YOLOv8n, 50 epochs)
# Run 03_train_yolov12.ipynb (YOLOv12n, 50 epochs)
# Models and metrics saved to models/
```

### 3. Compare Results

```bash
# Run 04_compare_metrics.ipynb
# View comparison charts and recommendations
```

### 4. Deploy

```bash
make app  # or: python app.py
# Upload X-rays at http://localhost:7860
```

---

## 📊 Features

- **Roboflow Integration**: One-click dataset download
- **Dual Model Comparison**: YOLOv8n vs YOLOv12n
- **Comprehensive Metrics**: Training time, params, speed, mAP
- **Interactive UI**: Gradio web interface
- **Docker Ready**: Consistent deployment

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
