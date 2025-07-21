# spark_jobs/transform_chlorophyll.py

from graphql.spark_utils.session import get_spark_session
from graphql.spark_utils.hdfs_helpers import write_to_hdfs
from graphql.utils.api_requests import fetch_chlorophyll_data
from pyspark.sql import functions as F

def transform_chlorophyll():
    spark = get_spark_session("Chlorophyll Data Transformation Job")

    # Parameters (adjust dates as required)
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    # Extract data from Chlorophyll API
    raw_chlorophyll_data = fetch_chlorophyll_data(start_date, end_date)

    schema = ["time", "latitude", "longitude", "chlorophyll_a"]
    df = spark.createDataFrame(raw_chlorophyll_data, schema=schema)

    # Transformation: clean, cast, aggregate daily data to weekly means
    df_transformed = (
        df.withColumn("time", F.to_timestamp("time"))
          .withColumn("chlorophyll_a", F.col("chlorophyll_a").cast("float"))
          .withColumn("week_start", F.date_trunc("week", "time"))
          .groupBy("week_start")
          .agg(F.avg("chlorophyll_a").alias("avg_chlorophyll_a"))
    )

    # Write transformed data to HDFS
    write_to_hdfs(df_transformed, "/data/chlorophyll/weekly_aggregated.parquet")

    spark.stop()

if __name__ == "__main__":
    transform_chlorophyll()
