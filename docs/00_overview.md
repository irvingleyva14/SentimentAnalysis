# Descripción general del proyecto

Este proyecto implementa una **API de análisis de sentimiento** utilizando **FastAPI** y un modelo preentrenado de **Hugging Face Transformers**.  
La arquitectura sigue los principios de **alta cohesión, bajo acoplamiento y mantenibilidad**, permitiendo un flujo limpio desde la solicitud HTTP hasta la inferencia del modelo.

La API puede ejecutarse:
- Localmente (con `uvicorn`).
- En un contenedor Docker.
- En la nube mediante **Google Cloud Run**, cargando el modelo desde almacenamiento local o desde un **bucket de Google Cloud Storage (GCS)**.

## Objetivos principales

- Exponer un endpoint REST para análisis de texto.
- Evitar recargas innecesarias del modelo (patrón Singleton).
- Facilitar el despliegue automatizado mediante scripts y contenedores.
- Garantizar la portabilidad y reproducibilidad del entorno.

## Tecnologías

- **FastAPI** – Framework backend principal.
- **Transformers (Hugging Face)** – Modelo de clasificación de texto.
- **Python 3.11**
- **Docker** – Contenerización del entorno.
- **Google Cloud Run** – Despliegue escalable sin servidor.
- **Google Cloud Storage (GCS)** – Almacenamiento del modelo.


This project provides a multilingual sentiment analysis API built with FastAPI.  
The model is loaded from a Google Cloud Storage bucket to optimize performance and avoid repeated downloads.

Main features:
- REST API built with FastAPI.
- Model served from GCS (bucket-based).
- Containerized using Docker.
- Deployed on Cloud Run.