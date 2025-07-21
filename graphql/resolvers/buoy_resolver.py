import graphene
import logging
from graphql import GraphQLError
from pyspark.sql.functions import col, to_timestamp, concat_ws
from spark_utils import get_spark_session, write_to_hdfs, hdfs_file_exists
from utils import fetch_buoy_data

logger = logging.getLogger(__name__)

class BuoyData(graphene.ObjectType):
    timestamp = graphene.DateTime()
    wave_height = graphene.Float()
    sst = graphene.Float()
    air_temp = graphene.Float()
    atmospheric_pressure = graphene.Float()
    station = graphene.String()

def resolve_buoy_data(root, info, station_id, limit=100):
    spark = info.context['spark']  # Persistent Spark session
    hdfs_path = f"/data/buoy/{station_id}.parquet"

    try:
        if not hdfs_file_exists(spark, hdfs_path):
            logger.warning(f"Preprocessed Buoy data not found at {hdfs_path}")
            raise GraphQLError("Preprocessed Buoy data not available.")

        logger.info(f"Loading buoy data from HDFS: {hdfs_path}")
        df = spark.read.parquet(hdfs_path)
        return df.limit(limit).collect()

    except GraphQLError as e:
        logger.error(f"GraphQL error in buoy resolver: {str(e)}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in buoy resolver: {str(e)}")
        raise GraphQLError("Internal server error during buoy data resolution.")


