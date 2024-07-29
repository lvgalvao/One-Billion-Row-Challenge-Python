from pyspark.sql import SparkSession
from pyspark.sql.functions import col, min, max, avg

spark = SparkSession.builder \
    .appName("read_billion_lines") \
    .config("spark.sql.shuffle.partitions", "8") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "6g") \
    .getOrCreate()

def create_spark():
    file_path = "data/measurements.txt"
    colums=["station", "temperature"]

    df = spark.read.csv(file_path, sep= ";", header=False, inferSchema=True).toDF(*colums)

    df = df.repartition(8)

    df.groupBy("station") \
                  .agg(
                      min("temperature").alias("min_temperature"),
                      avg("temperature").cast("decimal(3,1)").alias("mean_temperature"),
                      max("temperature").alias("max_temperature")
                  ) \
                  .orderBy("station").show()
    


if __name__ == "__main__":
    import time
    start_time = time.time()
    create_spark()
    took = time.time() - start_time
    spark.stop()
    print(f"Spark Took: {took:.2f} sec")