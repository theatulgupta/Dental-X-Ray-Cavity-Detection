# 🦷 Dental X-Ray Cavity Detection - Team Collaboration Guide

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Docker Workflow](#docker-workflow)
- [Team Workflow](#team-workflow)
- [Commands Reference](#commands-reference)
- [CI/CD Pipeline](#cicd-pipeline)
- [Deployment](#deployment)

---

## 🚀 Quick Start

### For New Team Members

```bash
# Clone the repository
git clone https://github.com/theatulgupta/Dental-X-Ray-Cavity-Detection.git
cd Dental-X-Ray-Cavity-Detection

# Run quick start (interactive)
chmod +x quick_start.sh
./quick_start.sh

# Or use Makefile
make help  # See all available commands
```

---

## 💻 Development Setup

### Option 1: Local Development (Python venv)

**Recommended for:** Day-to-day development, notebook work, quick iterations

```bash
# Automated setup
make setup

# Or manual setup
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install
```

**Activate environment:**

```bash
source venv/bin/activate
```

**Benefits:**

- ✅ Fast iteration
- ✅ Direct IDE integration
- ✅ Familiar Python workflow

---

### Option 2: Docker Development

**Recommended for:** Ensuring consistency, GPU training, production testing

```bash
# Build all images
make docker-build

# Start development environment (includes Jupyter)
make docker-up-dev

# Access services
# - Jupyter Lab: http://localhost:8888
# - Gradio App: http://localhost:7860
```

**Benefits:**

- ✅ Identical environment for all team members
- ✅ GPU support pre-configured
- ✅ Production parity
- ✅ No dependency conflicts

---

## 🐳 Docker Workflow

### Available Docker Services

1. **Development (`dev`)**: Full development environment with Jupyter

   ```bash
   make docker-up-dev
   ```

2. **Training (`train`)**: GPU-enabled training environment

   ```bash
   make train-docker
   ```

3. **Production App (`app`)**: Optimized Gradio interface
   ```bash
   make docker-up-app
   ```

### Common Docker Commands

```bash
# Build images
make docker-build

# Start all services
make docker-up

# Stop all services
make docker-down

# View logs
make docker-logs

# Open shell in container
make docker-shell-dev

# Clean everything
make docker-clean
```

---

## 👥 Team Workflow

### Git Branch Strategy

```
main (production)
  └── develop (integration)
       ├── feature/cavity-detection
       ├── feature/model-training
       └── bugfix/inference-fix
```

### Daily Development Flow

1. **Pull latest changes**

   ```bash
   git checkout develop
   git pull origin develop
   ```

2. **Create feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Activate environment**

   ```bash
   source venv/bin/activate  # or use Docker
   ```

4. **Make changes & commit**

   ```bash
   # Code formatting (automatic with pre-commit)
   make format

   # Run tests
   make test

   # Commit (pre-commit hooks run automatically)
   git add .
   git commit -m "feat: your feature description"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   # Create Pull Request on GitHub
   ```

---

## 📝 Commands Reference

### Code Quality

```bash
make format      # Auto-format code (black + isort)
make lint        # Run all linters
make test        # Run tests with coverage
make test-quick  # Run tests without coverage
make pre-commit  # Run pre-commit hooks manually
```

### Training

```bash
make train-yolov8   # Train YOLOv8 locally
make train-yolov12  # Train YOLOv12 locally
make train-docker   # Train with Docker (GPU)
```

### Application

```bash
make run-app        # Run Gradio app
make run-jupyter    # Run Jupyter Lab
```

### Data Processing

```bash
make prepare-data      # Prepare and split dataset
make compare-models    # Compare model performance
make inference-benchmark  # Run benchmarks
```

### Utilities

```bash
make clean       # Clean cache and temp files
make check-env   # Check environment setup
make help        # Show all commands
```

---

## 🔄 CI/CD Pipeline

### Automated Workflows

Our CI/CD pipeline runs on every push and PR:

#### 1. **Code Quality Check** (`lint`)

- Black formatting
- Flake8 linting
- isort import ordering
- MyPy type checking

#### 2. **Testing** (`test`)

- Unit tests with pytest
- Coverage reports
- Upload to Codecov

#### 3. **Docker Build** (`build`)

- Build multi-stage images
- Push to Docker Hub (on main branch)
- Tag with commit SHA

#### 4. **Security Scan** (`security`)

- Trivy vulnerability scanning
- SARIF reports to GitHub Security

#### 5. **Deployment** (`deploy`)

- Auto-deploy to Hugging Face Spaces (main branch only)

### Manual Training Workflow

Trigger model training via GitHub Actions:

1. Go to **Actions** tab
2. Select **"Model Training Pipeline"**
3. Click **"Run workflow"**
4. Choose model (yolov8/yolov12), epochs, batch size
5. Download artifacts after completion

---

## 🚀 Deployment

### Hugging Face Spaces

#### Setup Secrets (One-time)

Add these secrets to your GitHub repository:

```
Settings → Secrets → Actions → New repository secret
```

Required secrets:

- `HF_TOKEN`: Your Hugging Face access token
- `HF_SPACE_NAME`: Your space name (e.g., `username/dental-xray-detection`)
- `DOCKER_USERNAME`: Docker Hub username (optional)
- `DOCKER_PASSWORD`: Docker Hub password (optional)

#### Automatic Deployment

Deploys automatically when you push to `main`:

```bash
git checkout main
git merge develop
git push origin main
# CI/CD pipeline deploys automatically
```

#### Manual Deployment

```bash
export HF_TOKEN=your_token
export HF_SPACE_NAME=username/space-name
make deploy-hf
```

---

## 🗂️ Project Structure

```
dental-xray-cavity-detection/
├── .github/workflows/       # CI/CD pipelines
├── config/                  # Configuration files
├── data/                    # Dataset (gitignored)
├── models/                  # Trained models
├── notebooks/              # Jupyter notebooks
├── results/                # Training logs & metrics
├── scripts/                # Utility scripts
├── src/                    # Source code
│   ├── app/               # Gradio application
│   ├── data_prep/         # Data preprocessing
│   ├── evaluation/        # Model evaluation
│   └── training/          # Training scripts
├── tests/                  # Unit tests
├── .dockerignore          # Docker ignore rules
├── .flake8                # Flake8 configuration
├── .gitignore             # Git ignore rules
├── .pre-commit-config.yaml # Pre-commit hooks
├── .python-version        # Python version
├── docker-compose.yml     # Docker orchestration
├── Dockerfile             # Multi-stage Docker build
├── Makefile              # Command shortcuts
├── pyproject.toml        # Python project config
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
└── README.md             # This file
```

---

## 🛠️ Troubleshooting

### Common Issues

**1. Import errors after pulling changes**

```bash
pip install -r requirements.txt
```

**2. Pre-commit hooks failing**

```bash
make format  # Auto-fix formatting
pre-commit run --all-files
```

**3. Docker build fails**

```bash
make docker-clean
make docker-build
```

**4. CUDA/GPU issues**

```bash
# Check GPU availability
python -c "import torch; print(torch.cuda.is_available())"

# Use Docker for consistent GPU setup
make train-docker
```

**5. Port already in use**

```bash
# Change port in docker-compose.yml or app.py
# Or kill existing process
lsof -ti:7860 | xargs kill -9
```

---

## 📊 Code Quality Standards

### Formatting

- **Line length:** 120 characters
- **Formatter:** Black
- **Import sorting:** isort (black profile)

### Testing

- **Minimum coverage:** 80%
- **Framework:** pytest
- All new features must include tests

### Git Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature
fix: bug fix
docs: documentation changes
style: formatting changes
refactor: code refactoring
test: add/update tests
chore: maintenance tasks
```

---

## 🤝 Contributing

1. **Create an issue** describing the feature/bug
2. **Get assignment** from team lead
3. **Create feature branch** from `develop`
4. **Make changes** following code standards
5. **Run tests** and ensure they pass
6. **Create Pull Request** with description
7. **Request review** from team members
8. **Address feedback** and merge

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/theatulgupta/Dental-X-Ray-Cavity-Detection/issues)
- **Discussions:** [GitHub Discussions](https://github.com/theatulgupta/Dental-X-Ray-Cavity-Detection/discussions)
- **Team Lead:** [@theatulgupta](https://github.com/theatulgupta)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ by the Dental AI Team**
