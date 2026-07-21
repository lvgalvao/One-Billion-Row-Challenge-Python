from pyspark.sql import SparkSession
from pyspark.sql.functions import min, max, avg
import time
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
import sys
sys.stdout.reconfigure(encoding="utf-8")

def create_spark_df():

    spark = (
        SparkSession.builder
        .appName("One Billion Row Challenge")
        .getOrCreate()
    )

    schema = StructType([
    StructField("station", StringType(), True),
    StructField("temperature", DoubleType(), True)
    ])


    df = (
        spark.read
        .option("delimiter", ";")
        .option("header", "false")
        .schema(schema)
        .csv("data/measurements.txt")
    )

    df = df.toDF("station", "temperature")

    result = (
        df.groupBy("station")
        .agg(
            min("temperature").alias("min_temperature"),
            avg("temperature").alias("mean_temperature"),
            max("temperature").alias("max_temperature")
        )
        .orderBy("station")
    )

    return spark, result


if __name__ == "__main__":

    start_time = time.time()

    spark, result = create_spark_df()

    result.show()

    took = time.time() - start_time

    print(f"Spark Took: {took:.2f} sec")

    spark.stop()