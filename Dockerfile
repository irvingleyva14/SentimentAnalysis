# ===========================
# STAGE 1 - BUILDER
# Objetivo: Instalar compiladores para PyTorch/Pydantic y descargar dependencias.
# ===========================
FROM python:3.12-slim AS builder

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema para compilación (build-essential, gcc) y librerías de runtime
# Estas librerías se usarán para la compilación y serán eliminadas en el Stage 2.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libgomp1 libstdc++6 && \
    rm -rf /var/lib/apt/lists/*

# Copiar dependencias
COPY requirements.txt .

# Instalar todas las dependencias en un directorio local
# Ya no usamos --only-binary :all: ya que la base slim las gestiona.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --target /app/site-packages

# Copiar el código fuente completo (incluye app/, tests/, etc.)
COPY . /app

# ===========================
# STAGE 2 - RUNNER (IMAGEN HARDENED DE PRODUCCIÓN)
# Objetivo: Garantizar compatibilidad C/C++ y mantener la seguridad Non-root/Sin compiladores.
# ===========================
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar el código y los paquetes desde el Stage 1
COPY --from=builder /app /app

# 🧹 LIMPIEZA CRÍTICA: Eliminar herramientas de desarrollo (Requisito del examen)
# Mantenemos libstdc++6 y libgomp1, ya que son librerías de runtime necesarias para PyTorch/Pydantic
# y APT se niega a eliminarlas por dependencia.
RUN apt-get update && apt-get remove --purge -y build-essential gcc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# 👤 SEGURIDAD: Crear y usar usuario no-root (UID 10001) (Requisito del examen)
RUN groupadd -r appuser && useradd -r -g appuser -u 10001 appuser
USER 10001

# Configuración de entorno
ENV PYTHONPATH=/app/site-packages
ENV PORT=8080

# Exponer el puerto
EXPOSE 8080

# Healthcheck Nativo (Requisito del examen)
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c 'import urllib.request; urllib.request.urlopen("http://localhost:8080/health").getcode()'

# ENTRYPOINT y CMD (Ejecución de Gunicorn)
# Usamos la ruta absoluta de python para mayor robustez
ENTRYPOINT ["/usr/local/bin/python"]
CMD ["-m", "gunicorn", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--workers", "2", \
     "--threads", "1", \
     "--bind", "0.0.0.0:8080", \
     "app.main:app"]