# Etapa base
FROM python:3.11-slim

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1
ENV GOOGLE_CLOUD_PROJECT=professional-task

# Crear y usar un directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer puerto
EXPOSE 8080

# Comando para ejecutar la app
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["python", "run.py"]

