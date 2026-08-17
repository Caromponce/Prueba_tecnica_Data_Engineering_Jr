"""
Helper para crear una SparkSession con Delta Lake configurado.

Se centraliza acá para no repetir esta configuración en cada notebook:
si mañana hay que cambiar una config de Spark, se cambia en un solo lugar.
"""
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip


def get_spark(app_name: str = "prueba-tecnica-apex") -> SparkSession:
    """
    Crea (o reutiliza, si ya existe una activa) una SparkSession con las
    extensiones de Delta Lake habilitadas.

    Parámetros
    ----------
    app_name: nombre visible en la Spark UI (http://localhost:4040)
    """
    builder = (
        SparkSession.builder.appName(app_name)
        # Habilita la sintaxis SQL de Delta (MERGE, etc.) y el catálogo de Delta
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        # Por defecto Spark usa 200 particiones de shuffle, pensado para clusters
        # grandes. Con datos de juguete (4-5 filas) eso genera 200 archivos chiquitos
        # y hace que todo se sienta lento. 4 alcanza para este proyecto.
        .config("spark.sql.shuffle.partitions", "4")
        # Evita que Spark intente detectar el nivel de paralelismo de un cluster
        # real; local[*] usa todos los cores disponibles del contenedor.
        .master("local[*]")
    )

    # configure_spark_with_delta_pip() agrega automáticamente los JARs de Delta
    # (los descarga de Maven la primera vez que se llama; luego quedan cacheados
    # en el volumen spark-ivy-cache definido en docker-compose.yml).
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")  # silencia el ruido de INFO de Spark
    return spark
