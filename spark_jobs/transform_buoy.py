# spark_jobs/transform_buoy.py

from graphql.spark_utils.session import get_spark_session
from graphql.spark_utils.hdfs_helpers import write_to_hdfs
from graphql.utils.api_requests import fetch_buoy_data
from pyspark.sql import functions as F

def transform_buoy():
    spark = get_spark_session("Buoy Data Transformation Job")

    # Parameters (Wave Organ Buoy ID)
    station_id = "46026"

    # Extract data from Buoy API
    raw_buoy_lines = fetch_buoy_data(station_id)
    rdd = spark.sparkContext.parallelize([line.split() for line in raw_buoy_lines])

    schema = [
        "year", "month", "day", "hour", "minute", "wave_height",
        "sst", "air_temp", "atmospheric_pressure", "station"
    ]
    df = spark.createDataFrame(rdd, schema=schema)

    # Transformation: clean, cast types, aggregate hourly data to weekly means
    df_transformed = (
        df.withColumn(
            "timestamp",
            F.to_timestamp(F.concat_ws(" ", "year", "month", "day", "hour", "minute"), "yyyy MM dd HH mm")
        )
        .withColumn("wave_height", F.col("wave_height").cast("float"))
        .withColumn("sst", F.col("sst").cast("float"))
        .withColumn("air_temp", F.col("air_temp").cast("float"))
        .withColumn("atmospheric_pressure", F.col("atmospheric_pressure").cast("float"))
        .withColumn("week_start", F.date_trunc("week", "timestamp"))
        .groupBy("week_start")
        .agg(
            F.avg("wave_height").alias("avg_wave_height"),
            F.avg("sst").alias("avg_sst"),
            F.avg("air_temp").alias("avg_air_temp"),
            F.avg("atmospheric_pressure").alias("avg_atm_pressure")
        )
    )

    # Write transformed data to HDFS
    write_to_hdfs(df_transformed, "/data/buoy/weekly_aggregated.parquet")

    spark.stop()

if __name__ == "__main__":
    transform_buoy()
