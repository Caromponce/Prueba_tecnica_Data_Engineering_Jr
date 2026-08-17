# Imagen base: Python 3.11 (PySpark 3.5 no soporta bien 3.13, que es lo que tiene el host Windows).
# Se fija a "bookworm" (Debian 12) en vez de dejar la tag flotante "slim": la versión
# "trixie" más nueva ya no trae openjdk-17 en sus repos (solo openjdk-21), y Spark 3.5
# certifica Java 17 como la versión estable.
FROM python:3.11-slim-bookworm

# Spark 3.5 necesita Java 17 (el host tiene Java 8, por eso todo corre adentro del contenedor)
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jre-headless procps && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"
# Evita que Spark/Ivy tire warnings de zona horaria al resolver los JARs de Delta
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# El contenedor queda vivo esperando comandos (docker compose run / VS Code Dev Containers)
CMD ["sleep", "infinity"]
