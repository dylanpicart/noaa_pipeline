# spark_jobs/transform_pmn.py

from graphql.spark_utils.session import get_spark_session
from graphql.spark_utils.hdfs_helpers import write_to_hdfs
from graphql.utils.api_requests import fetch_pmn_data
from pyspark.sql import functions as F

def transform_pmn():
    spark = get_spark_session("PMN Data Transformation Job")

    # Extract data from PMN API
    raw_pmn_data = fetch_pmn_data()

    schema = ["time", "latitude", "longitude", "count", "water_temp", "salinity"]
    df = spark.createDataFrame(raw_pmn_data, schema=schema)

    # Transformation: clean data, cast types, aggregate weekly
    df_transformed = (
        df.withColumn("time", F.to_timestamp("time"))
          .withColumn("count", F.col("count").cast("float"))
          .withColumn("water_temp", F.col("water_temp").cast("float"))
          .withColumn("salinity", F.col("salinity").cast("float"))
          .withColumn("week_start", F.date_trunc("week", "time"))
          .groupBy("week_start")
          .agg(
              F.avg("count").alias("avg_pmn_count"),
              F.avg("water_temp").alias("avg_water_temp"),
              F.avg("salinity").alias("avg_salinity"),
              F.count("count").alias("measurement_count")
          )
          .filter(F.col("measurement_count") > 0)
    )

    # Write aggregated and transformed data to HDFS
    write_to_hdfs(df_transformed, "/data/pmn/weekly_aggregated.parquet")

    spark.stop()

if __name__ == "__main__":
    transform_pmn()