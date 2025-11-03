# Multi-stage Dockerfile for Dental X-Ray Cavity Detection
# Optimized for production deployment

# ============================================
# Stage 1: Base Image with System Dependencies
# ============================================
FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ============================================
# Stage 2: Development Image
# ============================================
FROM base as development

# Install development dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    nano \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir \
    jupyter \
    ipykernel \
    black \
    flake8 \
    pytest \
    pytest-cov

# Copy entire project
COPY . .

# Expose Jupyter and Gradio ports
EXPOSE 8888 7860

CMD ["bash"]

# ============================================
# Stage 3: Training Image (GPU Support)
# ============================================
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 as training

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

# Install Python 3.10
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu118 && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code and configs
COPY src/ ./src/
COPY config/ ./config/
COPY data/ ./data/

# Create directories for outputs
RUN mkdir -p models results/training_logs results/metrics

CMD ["python3", "-m", "src.training.train_yolov8"]

# ============================================
# Stage 4: Production Image (Inference Only)
# ============================================
FROM base as production

# Copy only requirements (smaller image)
COPY requirements.txt .

# Install only necessary production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/models /app/data && \
    chown -R appuser:appuser /app

USER appuser

# Copy only necessary files
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser config/ ./config/
COPY --chown=appuser:appuser app.py .
# Models should be mounted as volumes or downloaded at runtime

# Expose Gradio port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the Gradio app
CMD ["python", "app.py"]
