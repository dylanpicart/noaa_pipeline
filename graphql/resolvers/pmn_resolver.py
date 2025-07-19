import graphene
import logging
from graphql import GraphQLError
from pyspark.sql.functions import col, to_timestamp
from spark_utils import get_spark_session, hdfs_file_exists, write_to_hdfs
from utils import fetch_pmn_data

logger = logging.getLogger(__name__)

class PMNData(graphene.ObjectType):
    time = graphene.DateTime()
    altitude = graphene.Float()
    latitude = graphene.Float()
    longitude = graphene.Float()
    fluorescence = graphene.Float()

def resolve_pmn_data(limit=100):
    spark = get_spark_session()
    hdfs_path = "/data/pmn_data.parquet"

    try:
        if hdfs_file_exists(spark, hdfs_path):
            logger.info(f"Loading PMN data from HDFS: {hdfs_path}")
            df = spark.read.parquet(hdfs_path)
            return df.limit(limit).collect()

        raw_data = fetch_pmn_data()
        if not raw_data:
            logger.warning("PMN API returned empty data.")
            raise GraphQLError("PMN API returned no data.")

        schema = ["time", "altitude", "latitude", "longitude", "fluorescence"]
        rdd = spark.sparkContext.parallelize(raw_data)
        df = spark.createDataFrame(rdd, schema=schema)

        df_clean = (
            df.withColumn("time", to_timestamp("time"))
              .withColumn("fluorescence", col("fluorescence").cast("float"))
              .filter(col("latitude").isNotNull() & col("longitude").isNotNull())
        )

        logger.info(f"PMN data row count after cleaning: {df_clean.count()}")

        write_to_hdfs(df_clean, hdfs_path)
        logger.info(f"PMN data successfully cached to HDFS at {hdfs_path}")

        return df_clean.limit(limit).collect()

    except GraphQLError as e:
        logger.error(f"GraphQL error in PMN resolver: {str(e)}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in PMN resolver: {str(e)}")
        raise GraphQLError("Internal server error during PMN data resolution.")
