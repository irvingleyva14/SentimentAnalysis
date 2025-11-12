# Referencia de la API

## Endpoint principal

### `POST /predict/`

Realiza una predicción de sentimiento para un texto dado.

#### Request

**Ejemplo 1 (Query parameter):**

POST /predict?text=Me encanta este proyecto


**Ejemplo 2 (Body JSON, si se actualiza el endpoint):**
```json
{
  "text": "Me encanta este proyecto"
}


Response:

{
  "input_text": "Me encanta este proyecto",
  "sentiment": [
    {
      "label": "POSITIVE",
      "score": 0.98
    }
  ]
}

| Código | Descripción                   |
| ------ | ----------------------------- |
| 200    | Predicción exitosa            |
| 422    | Error de validación del input |
| 500    | Error interno del servidor    |


Documentación interactiva

Disponible en /docs (Swagger UI) y /redoc (ReDoc).