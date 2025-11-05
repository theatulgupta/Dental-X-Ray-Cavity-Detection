.PHONY: help build up down app jupyter train-v8 train-v12 clean

help:
	@echo "Docker Commands:"
	@echo "  make build      - Build Docker images"
	@echo "  make app        - Run Gradio app (http://localhost:7860)"
	@echo "  make jupyter    - Run Jupyter notebooks (http://localhost:8888)"
	@echo "  make up         - Run both app and jupyter"
	@echo "  make down       - Stop all containers"
	@echo "  make train-v8   - Train YOLOv8 model"
	@echo "  make train-v12  - Train YOLOv12 model"
	@echo "  make clean      - Remove containers and images"

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

app:
	docker-compose up dental-app

jupyter:
	docker-compose up jupyter

train-v8:
	docker-compose run dental-app python -m src.training.train_yolov8

train-v12:
	docker-compose run dental-app python -m src.training.train_yolov12

clean:
	docker-compose down -v
	docker system prune -f
