# spark_jobs/transform_climate.py

from graphql.spark_utils.session import get_spark_session
from graphql.spark_utils.hdfs_helpers import write_to_hdfs
from graphql.utils.api_requests import fetch_climate_data
from pyspark.sql import functions as F

def transform_climate():
    spark = get_spark_session("Climate Data Transformation Job")

    # Parameters (adjust as needed)
    dataset_id = "tavg_land_ocean"
    location_id = "37.75,-122.84"
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    token = os.getenv("NOAA_TOKEN")

    # Extract data from Climate API
    raw_climate_data = fetch_climate_data(dataset_id, location_id, start_date, end_date, token)

    schema = ["date", "latitude", "longitude", "temperature_anomaly"]
    df = spark.createDataFrame(raw_climate_data, schema=schema)

    # Transformation: clean, cast, aggregate monthly anomaly to weekly averages
    df_transformed = (
        df.withColumn("date", F.to_date("date"))
          .withColumn("temperature_anomaly", F.col("temperature_anomaly").cast("float"))
          .withColumn("week_start", F.date_trunc("week", "date"))
          .groupBy("week_start")
          .agg(F.avg("temperature_anomaly").alias("avg_temperature_anomaly"))
    )

    # Write transformed data to HDFS
    write_to_hdfs(df_transformed, "/data/climate/weekly_aggregated.parquet")

    spark.stop()

if __name__ == "__main__":
    transform_climate()
