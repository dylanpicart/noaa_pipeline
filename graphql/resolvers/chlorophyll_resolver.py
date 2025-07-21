import graphene
import logging
from graphql import GraphQLError
from pyspark.sql.functions import col, to_timestamp
from spark_utils import get_spark_session, write_to_hdfs, hdfs_file_exists
from utils import fetch_chlorophyll_data

logger = logging.getLogger(__name__)

class ChlorophyllData(graphene.ObjectType):
    time = graphene.DateTime()
    latitude = graphene.Float()
    longitude = graphene.Float()
    chlorophyll_a = graphene.Float()

def resolve_chlorophyll_data(root, info, start_date, end_date, limit=100):
    spark = info.context['spark']  # Persistent Spark session
    hdfs_path = f"/data/chlorophyll/{start_date}_{end_date}.parquet"

    try:
        if not hdfs_file_exists(spark, hdfs_path):
            logger.warning(f"Preprocessed Chlorophyll data not found at {hdfs_path}")
            raise GraphQLError("Preprocessed Chlorophyll data not available.")

        logger.info(f"Loading Chlorophyll data from HDFS: {hdfs_path}")
        df = spark.read.parquet(hdfs_path)
        return df.limit(limit).collect()

    except GraphQLError as e:
        logger.error(f"GraphQL error in Chlorophyll resolver: {str(e)}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in Chlorophyll resolver: {str(e)}")
        raise GraphQLError("Internal server error during Chlorophyll data resolution.")

