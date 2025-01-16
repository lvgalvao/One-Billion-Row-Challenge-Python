from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import time

# Setei esses parâmetros para minha máquina
# Linux 11, 32Gb de RAM, processador AMD® Ryzen 7 5700u with radeon graphics × 16 
spark = SparkSession.builder \
    .appName("OneBillionRowChallenge") \
    .master("local[12]") \
    .config("spark.sql.shuffle.partitions", "16") \
    .config("spark.driver.memory", "24g") \
    .config("spark.executor.memory", "24g") \
    .config("spark.driver.maxResultSize", "8g") \
    .getOrCreate()

def processar_temperaturas(file_path):
    df = spark.read.csv(file_path, sep=';', header=False, inferSchema=True) \
    .toDF("station", "measure")
    
    df = df.repartition(16)

    df = df.groupBy("station") \
        .agg(
            F.min("measure").alias("min"),
            F.max("measure").alias("max"),
            F.mean("measure").alias("mean")
        ) \
        .orderBy("station") ##.show(5) # Vou exibir apenas os 5 primeiros registros
        
    return df


if __name__ == "__main__":
    file_path = "data/measurements.txt" 
    
    print("Iniciando o processamento do arquivo.")
    start_time = time.time()  # Tempo de início

    try:
        resultados = processar_temperaturas(file_path)

        end_time = time.time() # Tempo de término

    finally:
        spark.stop()
    
    print(resultados)
    print(f"\nProcessamento concluído em {end_time - start_time:.2f} segundos.")
