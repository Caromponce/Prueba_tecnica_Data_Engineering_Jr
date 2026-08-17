# Prueba técnica — Ingeniero de Datos Jr

Resolución de la prueba técnica usando **PySpark 3.5 + Delta Lake 3.2**, todo ejecutándose
dentro de un contenedor Docker para no depender de la instalación de Java/Python del host.

El enunciado original está en [prueba_tecnica_ingeniero_datos_jr.pdf](prueba_tecnica_ingeniero_datos_jr.pdf)
y la solución está repartida en tres notebooks, uno por ejercicio.

---

## Estructura del proyecto

```
.
├── .devcontainer/devcontainer.json   # Config para abrir el proyecto con VS Code Dev Containers
├── docker/Dockerfile                 # Imagen: Python 3.11 + Java 17 + PySpark + Delta
├── docker-compose.yml                # Servicio "spark", monta el repo en /workspace
├── requirements.txt                  # pyspark==3.5.3, delta-spark==3.2.0, ipykernel
├── data/
│   ├── bronze/customers.json         # Datos de entrada (extracto de MongoDB)
│   └── silver/                       # Salidas Delta (generadas; ignoradas por git)
├── notebooks/
│   ├── 01_bronze_to_silver.ipynb     # Ejercicio 1
│   ├── 02_merge_orders.ipynb         # Ejercicio 2
│   └── 03_incremental_load.ipynb     # Ejercicio 3
└── src/
    ├── common/spark_session.py       # get_spark(): SparkSession con Delta configurado
    └── smoke_test.py                 # Verifica que Spark + Delta funcionen
```

---

## Requisitos

- Docker Desktop (con Docker Compose)
- VS Code + extensión *Dev Containers* (opcional, pero es la forma más cómoda de correr los notebooks)

No hace falta instalar Python, Java ni Spark en la máquina: la imagen fija **Python 3.11** y
**Java 17**, que son las versiones que PySpark 3.5 certifica.

---

## Puesta en marcha

### 1. Construir la imagen

```bash
docker compose build
```

### 2. Verificar el entorno (smoke test)

Escribe y lee una tabla Delta de prueba. Si esto pasa, Spark, Java y los JARs de Delta están bien:

```bash
docker compose run --rm spark python src/smoke_test.py
```

Debería terminar con `SMOKE TEST OK: Spark + Delta funcionan correctamente.`

> La primera corrida descarga los JARs de Delta (~40 MB) desde Maven. Quedan cacheados en el
> volumen `spark-ivy-cache`, así que las siguientes son inmediatas.

### 3. Correr los notebooks

**Opción A — VS Code Dev Containers (recomendada):** abrir la carpeta y elegir
*Reopen in Container*. VS Code instala las extensiones de Python y Jupyter **dentro** del
contenedor y ofrece el kernel correcto (el Python 3.11 con PySpark, no el del host).

**Opción B — Jupyter en el contenedor:**

```bash
docker compose run --rm --service-ports spark python -m jupyter lab --ip=0.0.0.0 --allow-root --no-browser
```

En cualquier caso, la Spark UI queda en <http://localhost:4040> mientras haya una sesión activa.

