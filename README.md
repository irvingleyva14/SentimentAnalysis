# 🧠 Sentiment Analysis API

API de análisis de sentimiento basada en un modelo de **Hugging Face Transformers**, desarrollada con **FastAPI** bajo los principios de **arquitectura limpia** y **alta cohesión / bajo acoplamiento**.

El proyecto está optimizado para uso local o despliegue en **Google Cloud Run**, cargando el modelo desde el almacenamiento local o desde un bucket de GCS para mejorar el rendimiento.

---

## 🚀 Características principales

- 🔹 API REST construida con **FastAPI**
- 🔹 Carga eficiente del modelo mediante un **servicio singleton**
- 🔹 Estructura modular y extensible
- 🔹 Logging centralizado
- 🔹 Documentación técnica completa en `/docs`
- 🔹 Preparado para despliegue en **Cloud Run**

---

## 🧱 Estructura del proyecto

project-root/
├── app/
│ ├── api/
│ │ ├── routes/
│ │ │ └── predict.py → Endpoint principal de predicción
│ │ └── dependencies.py → Inyección de dependencias
│ ├── core/
│ │ └── logger.py → Configuración central de logging
│ ├── services/
│ │ ├── model_loader.py → Carga y cacheo del modelo
│ │ └── predictor_service.py → Lógica de inferencia
│ └── init.py
│
├── models/
│ └── multilingual-sentiment/ → Modelo descargado localmente
│
├── docs/ → Documentación técnica
│ ├── 00_overview.md
│ ├── 01_architecture.md
│ ├── 02_decisions.md
│ ├── 03_api_reference.md
│ ├── 04_deployment.md
│ └── 05_future_work.md
│
├── main.py → Punto de entrada FastAPI
├── requirements.txt
└── README.md



---

## ⚙️ Instalación y ejecución local

### 1️⃣ Clonar el repositorio

```bash
git clone https://https://github.com/irvingleyva14/
cd SentimentAnalysis

2️⃣ Crear y activar un entorno virtual
python3 -m venv .venv
source .venv/bin/activate

3️⃣ Instalar dependencias
pip install -r requirements.txt

4️⃣ Ejecutar el servidor
uvicorn main:app --reload --port 8000

🧠 Ejemplo de uso
Endpoint /predict/
Request
curl -X POST "http://127.0.0.1:8000/predict?text=Me encanta este proyecto"

Response
{
  "input_text": "Me encanta este proyecto",
  "sentiment": [
    {
      "label": "POSITIVE",
      "score": 0.98
    }
  ]
}

🧩 Principios de diseño aplicados

Alta cohesión: cada módulo tiene una única responsabilidad.

Bajo acoplamiento: los servicios se comunican mediante dependencias inyectadas.

Reutilización: el modelo se carga una sola vez y permanece en memoria.

Escalabilidad: la API puede extenderse con nuevos modelos o endpoints fácilmente.



📚 Documentación técnica

Toda la documentación se encuentra en la carpeta /docs
:

Archivo	Contenido
00_overview.md	Descripción general del sistema
01_architecture.md	Estructura y flujo de la aplicación
02_decisions.md	Decisiones técnicas y de diseño
03_api_reference.md	Referencia detallada de endpoints
04_deployment.md	Guía de despliegue
05_future_work.md	Plan de mejoras futuras


🧑‍💻 Autor

Irving Leyva
Ingeniero en Mecatrónica con especialización en Inteligencia Artificial

“La claridad estructural precede a la eficiencia computacional.”

📜 Licencia

MIT License — libre para uso, modificación y distribución.
## 📚 Documentation

The documentation is divided into the following sections:

| File | Description |
|------|--------------|
| `docs/00_overview.md` | General overview of the project |
| `docs/01_architecture.md` | Project structure and components |
| `docs/02_decisions.md` | Technical design decisions |
| `docs/03_api_reference.md` | API endpoints and usage examples |
| `docs/04_deployment.md` | Deployment process and commands |
| `docs/05_future_work.md` | Planned improvements |

