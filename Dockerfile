# Etapa base
FROM python:3.11-slim

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1
ENV GOOGLE_CLOUD_PROJECT=professional-task

# Crear y usar un directorio de trabajo
WORKDIR /app

# Copiar dependencias primero
COPY requirements.txt /app/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código (incluyendo tests)
COPY . /app/

# Exponer puerto para Cloud Run
EXPOSE 8080

# Ejecutar la API en Cloud Run
CMD ["python", "run.py"]
