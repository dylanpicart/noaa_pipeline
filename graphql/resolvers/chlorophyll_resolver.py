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

def resolve_chlorophyll_data(start_date, end_date, limit=100):
    spark = get_spark_session()
    hdfs_path = f"/data/chlorophyll/{start_date}_{end_date}.parquet"

    try:
        if hdfs_file_exists(spark, hdfs_path):
            logger.info(f"Loading Chlorophyll data from HDFS: {hdfs_path}")
            df = spark.read.parquet(hdfs_path)
            return df.limit(limit).collect()

        raw_data = fetch_chlorophyll_data(start_date, end_date)
        if not raw_data:
            logger.warning("Chlorophyll API returned empty data.")
            raise GraphQLError("Chlorophyll API returned no data.")

        schema = ["time", "latitude", "longitude", "chlorophyll_a"]
        rdd = spark.sparkContext.parallelize(raw_data)
        df = spark.createDataFrame(rdd, schema=schema)

        df_clean = (
            df.withColumn("time", to_timestamp("time"))
              .withColumn("chlorophyll_a", col("chlorophyll_a").cast("float"))
              .filter(col("chlorophyll_a").isNotNull())
        )

        logger.info(f"Chlorophyll data rows after cleaning: {df_clean.count()}")

        write_to_hdfs(df_clean, hdfs_path)
        return df_clean.limit(limit).collect()

    except Exception as e:
        logger.exception(f"Error in Chlorophyll resolver: {str(e)}")
        raise GraphQLError("Internal server error during Chlorophyll data resolution.")
