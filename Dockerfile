# Imagen base
FROM python:3.10-slim

# Config
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Copiar archivos
COPY . /app

# Instalar torch desde el índice CPU
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Instalar el resto de dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto
EXPOSE 8080

# Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
