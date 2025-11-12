# Arquitectura del sistema

El proyecto sigue una arquitectura modular inspirada en los principios de **Clean Architecture**.

## Estructura general

app/
├── api/ → Endpoints y routers
├── core/ → Configuración, logging y constantes globales
├── services/ → Lógica de negocio e inferencia del modelo
└── models/ → Estructuras Pydantic y modelo descargado

## Flujo general de ejecución

1. El cliente realiza un `POST /predict` con texto.
2. FastAPI recibe el request y lo pasa al servicio de predicción.
3. El `PredictorService` carga el modelo (local o desde GCS).
4. Se ejecuta el pipeline `transformers.pipeline("text-classification")`.
5. Se devuelve una respuesta JSON con el sentimiento y la confianza.

## Principios aplicados

- **Alta cohesión:** cada módulo cumple un rol claro.
- **Bajo acoplamiento:** los servicios interactúan mediante inyección de dependencias.
- **Reutilización:** el modelo se carga una única vez.
- **Escalabilidad:** se pueden agregar nuevos endpoints o modelos fácilmente.
