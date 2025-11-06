# Arquitectura del sistema

La API está organizada según los principios de **Clean Architecture**:

app/
├── api/ → Controladores (routers, endpoints)
├── core/ → Configuración global, logging, etc.
├── services/ → Lógica de negocio y manejo de modelos
└── models/ → (opcional) esquemas Pydantic de entrada/salida


## Flujo general de ejecución

1. El cliente envía una solicitud `POST /predict` con un texto.
2. FastAPI inyecta una instancia de `PredictorService` mediante dependencias.
3. `PredictorService` usa `ModelLoader` para obtener el modelo desde `models/multilingual-sentiment`.
4. El modelo realiza la inferencia con `transformers.pipeline("text-classification")`.
5. Se devuelve la respuesta JSON con el sentimiento detectado.

## Principios aplicados

- **Alta cohesión**: cada módulo tiene una única responsabilidad.
- **Bajo acoplamiento**: los servicios interactúan a través de dependencias controladas.
- **Reutilización**: el modelo se carga una sola vez y se comparte entre requests.
- **Extensibilidad**: se puede agregar fácilmente un nuevo modelo o endpoint.

