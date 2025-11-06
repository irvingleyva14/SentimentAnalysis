# Descripción general del proyecto

Este proyecto implementa una **API de clasificación de texto** basada en un modelo de Hugging Face, utilizando **FastAPI** como framework principal y una arquitectura modular para garantizar mantenibilidad, cohesión y bajo acoplamiento.

El objetivo es exponer un endpoint REST que reciba texto y devuelva la predicción del sentimiento, aprovechando un modelo preentrenado almacenado localmente o en Google Cloud Storage (GCS).

## Objetivos principales

- Proveer un servicio de inferencia rápido y reutilizable.
- Evitar recargas innecesarias del modelo mediante una instancia singleton.
- Facilitar el despliegue en entornos como Cloud Run o Vertex AI.
- Mantener una estructura limpia, escalable y documentada.

## Tecnologías

- **FastAPI** – Framework backend para la API REST.
- **Transformers (Hugging Face)** – Carga y ejecución del modelo de clasificación.
- **Python 3.10+**
- **Google Cloud (opcional)** – Almacenamiento o despliegue en Cloud Run.
