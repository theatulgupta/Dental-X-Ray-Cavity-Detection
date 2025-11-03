# 🦷 Dental X-Ray Cavity Detection

A deep learning project to detect dental cavities from X-ray images using **YOLOv8** and **YOLOv12**, with a **Gradio web demo** for deployment on **Hugging Face Spaces**.

---

## 📋 Overview

This project compares two object detection models (**YOLOv8** and **YOLOv12**) trained on a public dental X-ray dataset. Users can upload an image via the web interface to detect and visualize cavities.

---

## 🧠 Features

- Train and evaluate YOLOv8 & YOLOv12 models on dental X-rays
- Dataset preprocessing and YOLO-format conversion
- Model comparison: parameters, training time, and inference speed
- Gradio web app for cavity detection
- Hugging Face Spaces deployment-ready

---

## 🗂️ Project Structure

```text
dental-xray-cavity-detection/
│
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── config/
│   ├── yolo_v8.yaml
│   ├── yolo_v12.yaml
│   └── app_config.yaml
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── annotations/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_yolov8_training.ipynb
│   ├── 04_yolov12_training.ipynb
│   ├── 05_inference_comparison.ipynb
│   └── 06_metrics_visualization.ipynb
│
├── src/
│   ├── data_prep/
│   │   ├── split_dataset.py
│   │   ├── convert_to_yolo_format.py
│   │   └── utils.py
│   │
│   ├── training/
│   │   ├── train_yolov8.py
│   │   ├── train_yolov12.py
│   │   └── model_utils.py
│   │
│   ├── evaluation/
│   │   ├── compare_models.py
│   │   ├── inference_benchmark.py
│   │   └── metrics_utils.py
│   │
│   ├── app/
│   │   ├── app.py
│   │   ├── inference.py
│   │   ├── visualize.py
│   │   └── helpers.py
│   │
│   └── deployment/
│       ├── hf_spaces_setup.md
│       └── requirements_spaces.txt
│
├── models/
│   ├── yolov8_best.pt
│   ├── yolov12_best.pt
│   └── model_summary.json
│
├── results/
│   ├── training_logs/
│   ├── metrics/
│   │   ├── yolov8_results.json
│   │   └── yolov12_results.json
│   └── comparison_plot.png
│
└── app.py
```

---

## 🧩 Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/theatulgupta/Dental-X-Ray-Cavity-Detection.git
cd Dental-X-Ray-Cavity-Detection
```

### 2️⃣ Create and activate virtual environment

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Download dataset

Download the dataset from [Kaggle Dental X-ray Dataset](https://www.kaggle.com/datasets/killa92/dental-x-ray-images-dataset?resource=download) and place it inside:

```text
data/raw/
```

### 5️⃣ Run preprocessing

```bash
python src/data_prep/split_dataset.py
python src/data_prep/convert_to_yolo_format.py
```

### 6️⃣ Train models

```bash
python src/training/train_yolov8.py
python src/training/train_yolov12.py
```

### 7️⃣ Compare performance

```bash
python src/evaluation/compare_models.py
```

### 8️⃣ Launch web app

```bash
python app.py
```

---

## 🚀 Deployment (Hugging Face Spaces)

Follow the instructions in [`src/deployment/hf_spaces_setup.md`](src/deployment/hf_spaces_setup.md) to deploy the Gradio app to Hugging Face Spaces.

---

## 📊 Results

| Model   | Parameters | Training Time | Inference Time (avg/img) | mAP |
| ------- | ---------- | ------------- | ------------------------ | --- |
| YOLOv8  | —          | —             | —                        | —   |
| YOLOv12 | —          | —             | —                        | —   |

> **Note:** Results will be populated after training and evaluation.

---

## 📜 License

Licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to modify.

---

## 👨‍💻 Author's 

**Atul Kumar Gupta**  
Engineer | AI & Full Stack Developer  
🔗 [GitHub](https://github.com/theatulgupta) • [LinkedIn](https://linkedin.com/in/theatulgupta)

**Ankit Pawar**  
Engineer | AI & Full Stack Developer  
🔗 [GitHub](https://github.com/ankit8453) • [LinkedIn](https://linkedin.com/in/theatulgupta)

**Gourav Chouhan**  
Engineer | AI & Full Stack Developer  
🔗 [GitHub](https://github.com/theatulgupta) • [LinkedIn](https://linkedin.com/in/theatulgupta)

**Richa Verma**  
Engineer | AI & Full Stack Developer  
🔗 [GitHub](https://github.com/theatulgupta) • [LinkedIn](https://linkedin.com/in/theatulgupta)

---

---

dental-xray-cavity-detection/
│
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── config/
│ ├── yolo_v8.yaml
│ ├── yolo_v12.yaml
│ └── app_config.yaml
│
├── data/
│ ├── raw/
│ ├── processed/
│ └── annotations/
│
├── notebooks/
│ ├── 01_data_exploration.ipynb
│ ├── 02_preprocessing.ipynb
│ ├── 03_yolov8_training.ipynb
│ ├── 04_yolov12_training.ipynb
│ ├── 05_inference_comparison.ipynb
│ └── 06_metrics_visualization.ipynb
│
├── src/
│ ├── data_prep/
│ │ ├── split_dataset.py
│ │ ├── convert_to_yolo_format.py
│ │ └── utils.py
│ │
│ ├── training/
│ │ ├── train_yolov8.py
│ │ ├── train_yolov12.py
│ │ └── model_utils.py
│ │
│ ├── evaluation/
│ │ ├── compare_models.py
│ │ ├── inference_benchmark.py
│ │ └── metrics_utils.py
│ │
│ ├── app/
│ │ ├── app.py
│ │ ├── inference.py
│ │ ├── visualize.py
│ │ └── helpers.py
│ │
│ └── deployment/
│ ├── hf_spaces_setup.md
│ └── requirements_spaces.txt
│
├── models/
│ ├── yolov8_best.pt
│ ├── yolov12_best.pt
│ └── model_summary.json
│
├── results/
│ ├── training_logs/
│ ├── metrics/
│ │ ├── yolov8_results.json
│ │ ├── yolov12_results.json
│ └── comparison_plot.png
│
└── app.py

---

## 🧩 Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/dental-xray-cavity-detection.git
cd dental-xray-cavity-detection

2️⃣ Create and activate virtual environment

python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Download dataset

Download from Kaggle Dental X-ray Dataset￼
and place it inside:

data/raw/

5️⃣ Run preprocessing

python src/data_prep/split_dataset.py
python src/data_prep/convert_to_yolo_format.py

6️⃣ Train models

python src/training/train_yolov8.py
python src/training/train_yolov12.py

7️⃣ Compare performance

python src/evaluation/compare_models.py

8️⃣ Launch web app

python app.py


⸻

🚀 Deployment (Hugging Face Spaces)

Follow the instructions in:

src/deployment/hf_spaces_setup.md

to deploy the Gradio app to Hugging Face Spaces.

⸻

📊 Results

Model Parameters Training Time Inference Time (avg/img) mAP
YOLOv8 — — — —
YOLOv12 — — — —

(Results will be filled after training and evaluation.)

⸻

📜 License

Licensed under the MIT License — see LICENSE￼ for details.

⸻

🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first to discuss what you’d like to modify.

⸻

👨‍💻 Author

Atul Kumar Gupta
Engineer | AI & Full Stack Developer
🔗 GitHub￼ • LinkedIn￼

---
```
