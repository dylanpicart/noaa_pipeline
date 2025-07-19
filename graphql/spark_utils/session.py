from pyspark.sql import SparkSession
from .yarn import get_yarn_spark_config

def get_spark_session(app_name="NOAA GraphQL Server"):
    spark_builder = SparkSession.builder.appName(app_name)

    yarn_config = get_yarn_spark_config()
    for key, value in yarn_config.items():
        spark_builder.config(key, value)

    spark = spark_builder.getOrCreate()
    return spark
