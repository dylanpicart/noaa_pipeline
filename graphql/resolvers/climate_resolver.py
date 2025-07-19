import graphene
import logging
import os
from datetime import datetime
from graphql import GraphQLError
from spark_utils import get_spark_session, hdfs_file_exists, write_to_hdfs
from utils import setup_logging, fetch_climate_data

setup_logging()
logger = logging.getLogger(__name__)

NOAA_TOKEN = os.getenv("NOAA_TOKEN")

class ClimateData(graphene.ObjectType):
    date = graphene.String()
    datatype = graphene.String()
    value = graphene.Float()
    station = graphene.String()
    attributes = graphene.String()

def resolve_climate_data(dataset_id, location_id, start_date, end_date, limit=100):
    spark = get_spark_session()
    hdfs_path = f"/data/climate/{dataset_id}_{location_id}_{start_date}_{end_date}.parquet"

    start_date_str = start_date.isoformat() if isinstance(start_date, datetime) else start_date
    end_date_str = end_date.isoformat() if isinstance(end_date, datetime) else end_date

    try:
        if hdfs_file_exists(spark, hdfs_path):
            logger.info(f"Loading climate data from HDFS: {hdfs_path}")
            df = spark.read.parquet(hdfs_path)
            return df.limit(limit).collect()

        raw_data = fetch_climate_data(dataset_id, location_id, start_date_str, end_date_str, NOAA_TOKEN)
        if not raw_data:
            logger.warning("Climate API returned empty data.")
            raise GraphQLError("Climate API returned no data.")

        df = spark.createDataFrame(raw_data)
        
        logger.info(f"Climate data row count after retrieval: {df.count()}")

        write_to_hdfs(df, hdfs_path)
        logger.info(f"Climate data successfully cached to HDFS at {hdfs_path}")

        return [
            ClimateData(
                date=row.date,
                datatype=row.datatype,
                value=row.value,
                station=row.station,
                attributes=row.attributes
            ) for row in df.limit(limit).collect()
        ]

    except GraphQLError as e:
        logger.error(f"GraphQL error in climate resolver: {str(e)}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in climate resolver: {str(e)}")
        raise GraphQLError("Internal server error during climate data resolution.")
