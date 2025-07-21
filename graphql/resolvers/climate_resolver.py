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

def resolve_climate_data(root, info, dataset_id, location_id, start_date, end_date, limit=100):
    spark = info.context['spark']  # Persistent Spark session
    hdfs_path = f"/data/climate/{dataset_id}_{location_id}_{start_date}_{end_date}.parquet"

    try:
        if not hdfs_file_exists(spark, hdfs_path):
            logger.warning(f"Preprocessed Climate data not found at {hdfs_path}")
            raise GraphQLError("Preprocessed Climate data not available.")

        logger.info(f"Loading climate data from HDFS: {hdfs_path}")
        df = spark.read.parquet(hdfs_path)
        return df.limit(limit).collect()

    except GraphQLError as e:
        logger.error(f"GraphQL error in climate resolver: {str(e)}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in climate resolver: {str(e)}")
        raise GraphQLError("Internal server error during climate data resolution.")

