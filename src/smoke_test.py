"""
Smoke test del entorno: confirma que Spark + Delta Lake funcionan de punta a
punta ANTES de abrir VS Code. Si algo falla acá (Java, versiones, JARs de
Delta), el error se ve limpio en la terminal.

Se corre con:
    docker compose run --rm spark python src/smoke_test.py
"""
from src.common.spark_session import get_spark

if __name__ == "__main__":
    spark = get_spark("smoke-test")
    print(f"Spark version: {spark.version}")

    # DataFrame de prueba: 2 filas simples
    df = spark.createDataFrame(
        [(1, "hola"), (2, "delta")], schema=["id", "mensaje"]
    )

    ruta = "/workspace/data/silver/_smoke_test"
    df.write.format("delta").mode("overwrite").save(ruta)

    print("Escritura Delta OK. Leyendo de vuelta...")
    leido_df = spark.read.format("delta").load(ruta)
    leido_df.show()

    assert leido_df.count() == 2, "Se esperaban 2 filas"
    print("SMOKE TEST OK: Spark + Delta funcionan correctamente.")

    spark.stop()
