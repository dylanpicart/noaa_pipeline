import graphene
import logging
from graphql import GraphQLError
from pyspark.sql.functions import col, to_timestamp
from spark_utils import get_spark_session, hdfs_file_exists, write_to_hdfs
from utils import fetch_pmn_data

logger = logging.getLogger(__name__)

class PMNData(graphene.ObjectType):
    time = graphene.DateTime()
    latitude = graphene.Float()
    longitude = graphene.Float()
    count = graphene.Float()
    water_temp = graphene.Float()
    salinity = graphene.Float()

def resolve_pmn_data(root, info, limit=100):
    spark = info.context['spark']  # Persistent Spark session
    hdfs_path = "/data/pmn/weekly_aggregated.parquet"

    try:
        if not hdfs_file_exists(spark, hdfs_path):
            logger.warning(f"Preprocessed PMN data not found at {hdfs_path}")
            raise GraphQLError("Preprocessed PMN data not available.")

        logger.info(f"Loading PMN data from HDFS: {hdfs_path}")
        df = spark.read.parquet(hdfs_path)
        return df.limit(limit).collect()

    except GraphQLError as e:
        logger.error(f"GraphQL error in PMN resolver: {str(e)}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in PMN resolver: {str(e)}")
        raise GraphQLError("Internal server error during PMN data resolution.")

