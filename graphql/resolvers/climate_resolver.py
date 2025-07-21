import graphene
import logging
import os
from datetime import datetime
from graphql import GraphQLError
from pyspark.sql.functions import col, to_date
from spark_utils import get_spark_session, hdfs_file_exists, write_to_hdfs
from utils import setup_logging, fetch_climate_data

setup_logging()
logger = logging.getLogger(__name__)

NOAA_TOKEN = os.getenv("NOAA_TOKEN")

class ClimateData(graphene.ObjectType):
    date = graphene.Date()
    latitude = graphene.Float()
    longitude = graphene.Float()
    temperature_anomaly = graphene.Float()

def resolve_climate_data(dataset_id, location_id, start_date, end_date, limit=100):
    spark = get_spark_session()
    hdfs_path = f"/data/climate/{dataset_id}_{location_id}_{start_date}_{end_date}.parquet"

    try:
        if hdfs_file_exists(spark, hdfs_path):
            logger.info(f"Loading climate data from HDFS: {hdfs_path}")
            df = spark.read.parquet(hdfs_path)
            return df.limit(limit).collect()

        start_date_str = start_date.strftime("%Y-%m-%d") if isinstance(start_date, datetime) else str(start_date)
        end_date_str = end_date.strftime("%Y-%m-%d") if isinstance(end_date, datetime) else str(end_date)
        raw_data = fetch_climate_data(dataset_id, location_id, start_date_str, end_date_str, NOAA_TOKEN)
        if not raw_data:
            logger.warning("Climate API returned empty data.")
            raise GraphQLError("Climate API returned no data.")

        schema = ["date", "latitude", "longitude", "temperature_anomaly"]
        rdd = spark.sparkContext.parallelize(raw_data)
        df = spark.createDataFrame(rdd, schema=schema)

        df_clean = (
            df.withColumn("date", to_date("date"))
              .withColumn("latitude", col("latitude").cast("float"))
              .withColumn("longitude", col("longitude").cast("float"))
              .withColumn("temperature_anomaly", col("temperature_anomaly").cast("float"))
              .filter(col("temperature_anomaly").isNotNull())
        )

        logger.info(f"Climate data rows after cleaning: {df_clean.count()}")

        write_to_hdfs(df_clean, hdfs_path)
        logger.info(f"Climate data successfully cached to HDFS at {hdfs_path}")

        return df_clean.limit(limit).collect()

    except GraphQLError as e:
        logger.error(f"GraphQL error in climate resolver: {str(e)}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in climate resolver: {str(e)}")
        raise GraphQLError("Internal server error during climate data resolution.")
