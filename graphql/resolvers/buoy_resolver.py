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
    station = graphene.String()

def resolve_buoy_data(station_id, limit=100):
    spark = get_spark_session()
    hdfs_path = f"/data/buoy/{station_id}.parquet"

    try:
        if hdfs_file_exists(spark, hdfs_path):
            logger.info(f"Loading buoy data from HDFS: {hdfs_path}")
            df = spark.read.parquet(hdfs_path)
            return df.limit(limit).collect()

        raw_data = fetch_buoy_data(station_id)
        rdd = spark.sparkContext.parallelize([line.split() for line in raw_data])

        schema = ["year", "month", "day", "hour", "minute", "wave_height", "sst", "station"]
        df = spark.createDataFrame(rdd, schema=schema)

        df_clean = df.withColumn(
            "timestamp",
            to_timestamp(concat_ws(" ", "year", "month", "day", "hour", "minute"), "yyyy MM dd HH mm")
        ).withColumn("wave_height", col("wave_height").cast("float")) \
         .withColumn("sst", col("sst").cast("float")) \
         .filter(col("wave_height").isNotNull())

        write_to_hdfs(df_clean, hdfs_path)
        return df_clean.limit(limit).collect()

    except GraphQLError as e:
        logger.error(f"GraphQL error in buoy resolver: {str(e)}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in buoy resolver: {str(e)}")
        raise GraphQLError("Internal server error during buoy data resolution.")
