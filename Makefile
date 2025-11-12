# Variables
SERVICE_NAME = sentiment-api
REGION = northamerica-south1
PROJECT_ID = professional-task

# Comandos principales
run:
	uvicorn app.main:app --reload --port 8080

build:
	docker build -t $(SERVICE_NAME) .

push:
	docker tag $(SERVICE_NAME) gcr.io/$(PROJECT_ID)/$(SERVICE_NAME)
	docker push gcr.io/$(PROJECT_ID)/$(SERVICE_NAME)

deploy:
	./deploy.sh

clean:
	rm -rf __pycache__ */__pycache__ .pytest_cache .venv

help:
	@echo "Comandos disponibles:"
	@echo "  make run      -> Ejecutar localmente con uvicorn"
	@echo "  make build    -> Construir imagen Docker"
	@echo "  make push     -> Subir imagen al Container Registry"
	@echo "  make deploy   -> Desplegar en Cloud Run"
	@echo "  make clean    -> Limpiar archivos temporales"
