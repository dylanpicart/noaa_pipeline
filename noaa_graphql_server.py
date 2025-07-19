import os
import time
import logging
import requests
import graphene
import subprocess
from flask import Flask, jsonify
from flask_cors import CORS
from flask_graphql import GraphQLView
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, concat_ws, mean
from datetime import datetime
from graphql import GraphQLError
from py4j.protocol import Py4JJavaError

# Ensure Java Home and Path are set for Zulu11 JDK
os.environ["JAVA_HOME"] = "/usr/lib/jvm/zulu11"
os.environ["PATH"] = os.environ["JAVA_HOME"] + "/bin:" + os.environ["PATH"]

# Setup logging
logging.basicConfig(
    filename='/usr/local/hadoop/logs/noaa_graphql_server.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Spark-specific logger
spark_logger = logging.getLogger('spark_logger')
spark_handler = logging.FileHandler('/usr/local/hadoop/logs/spark_jobs.log')
spark_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
spark_logger.addHandler(spark_handler)
spark_logger.setLevel(logging.INFO)

# NOAA Token
NOAA_TOKEN = os.getenv("NOAA_TOKEN")
if not NOAA_TOKEN:
    logging.warning("NOAA_TOKEN not set. Please export it to the environment.")

# Flask app setup
app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify(status="healthy"), 200

# Spark session creation for YARN and HDFS
def create_spark_session():
    """Create and return a Spark session configured for YARN."""
    try:
        # Debug: print JAVA_HOME and test java call
        java_home = os.environ.get("JAVA_HOME", "NOT SET")
        print(f"[DEBUG] JAVA_HOME = {java_home}")
        subprocess.call("java -version", shell=True)

        spark = SparkSession.builder \
            .appName("NOAA GraphQL Server") \
            .master("yarn") \
            .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
            .config("spark.dynamicAllocation.enabled", "true") \
            .config("spark.executor.memory", "2g") \
            .config("spark.executor.cores", "2") \
            .config("spark.executor.instances", "4") \
            .config("spark.yarn.queue", "default") \
            .config("spark.yarn.am.memory", "1g") \
            .config("spark.executor.memoryOverhead", "512m") \
            .getOrCreate()

        spark_logger.info("SparkSession initialized successfully with YARN.")
        return spark

    except Exception as e:
        spark_logger.error(f"Error initializing SparkSession with YARN: {str(e)}")
        raise



# GraphQL Data Types
class PMNData(graphene.ObjectType):
    time = graphene.DateTime()
    altitude = graphene.Float()
    latitude = graphene.Float()
    longitude = graphene.Float()
    fluorescence = graphene.Float()

class BuoyData(graphene.ObjectType):
    timestamp = graphene.DateTime()
    wave_height = graphene.Float()
    sst = graphene.Float()
    station = graphene.String()

class ClimateData(graphene.ObjectType):
    date = graphene.String()
    datatype = graphene.String()
    value = graphene.Float()
    station = graphene.String()
    attributes = graphene.String()

# GraphQL Query Resolvers
class Query(graphene.ObjectType):
    get_pmn_data = graphene.List(PMNData)
    get_buoy_data = graphene.List(BuoyData, station_id=graphene.String(required=True))
    get_climate_data = graphene.List(
        ClimateData,
        dataset_id=graphene.String(required=True),
        location_id=graphene.String(required=True),
        start_date=graphene.DateTime(required=True),
        end_date=graphene.DateTime(required=True)
    )

    def resolve_get_pmn_data(self, info):
        url = (
            "https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMWcflhmday.json?"
            "fluorescence%5B(2024-08-16T12:00:00Z):1:(2024-09-15T12:00:00Z)%5D"
            "%5B(0.0):1:(0.0)%5D%5B(32):1:(49)%5D%5B(235):1:(243)%5D"
        )
        return fetch_and_transform_pmn_data(url)

    def resolve_get_buoy_data(self, info, station_id):
        url = f"https://www.ndbc.noaa.gov/data/realtime2/{station_id}.txt"
        return fetch_and_transform_buoy_data(url)

    def resolve_get_climate_data(self, info, dataset_id, location_id, start_date, end_date):
        return fetch_and_transform_climate_data(dataset_id, location_id, start_date, end_date)


# Helper Functions for HDFS operations
def write_to_hdfs(df, path):
    """Write a DataFrame to HDFS."""
    try:
        df.write.mode("overwrite").parquet(path)
        spark_logger.info(f"Data written to HDFS at {path}")
    except Exception as e:
        spark_logger.error(f"Error writing data to HDFS at {path}: {str(e)}")
        raise

def read_from_hdfs(path, spark):
    """Read a DataFrame from HDFS."""
    try:
        df = spark.read.parquet(path)
        spark_logger.info(f"Data read from HDFS at {path}")
        return df
    except Exception as e:
        spark_logger.error(f"Error reading data from HDFS at {path}: {str(e)}")
        raise
    
def hdfs_file_exists(spark, hdfs_path):
    """
    Check if a file or directory exists in HDFS.

    Parameters:
        spark (SparkSession): The active Spark session.
        hdfs_path (str): The HDFS path to check.

    Returns:
        bool: True if the file or directory exists, False otherwise.
    """
    try:
        # Get the Hadoop filesystem configuration from SparkSession
        hadoop_conf = spark._jsc.hadoopConfiguration()
        fs = spark._jvm.org.apache.hadoop.fs.FileSystem.get(hadoop_conf)

        # Check if the path exists in HDFS
        return fs.exists(spark._jvm.org.apache.hadoop.fs.Path(hdfs_path))
    except Py4JJavaError as e:
        spark_logger.error(f"Error checking HDFS path existence: {str(e)}")
        return False
    
    
def fetch_and_transform_pmn_data(url=None):
    """
    Fetch and transform PMN data using Spark and store results in HDFS.
    """
    spark = create_spark_session()
    hdfs_path = "/data/pmn_data.parquet"  # HDFS path for cached PMN data

    try:
        # If no URL is provided, use the default corrected URL
        if url is None:
            url = (
                "https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMWcflhmday.json?"
                "fluorescence%5B(2024-09-15T12:00:00Z):1:(2024-09-15T12:00:00Z)%5D"
                "%5B(0.0):1:(0.0)%5D%5B(32):1:(49)%5D%5B(235):1:(243)%5D"
            )

        # Check if data is already cached in HDFS
        if hdfs_file_exists(spark, hdfs_path):
            spark_logger.info("PMN data found in HDFS. Loading from cache.")
            df_cached = spark.read.parquet(hdfs_path)
            return df_cached.collect()

        # Fetch PMN data from the API
        response = requests.get(url)
        if response.status_code != 200:
            raise GraphQLError(f"Failed to fetch PMN data: {response.status_code}")

        # Process fetched data
        data = response.json()["table"]["rows"]
        rdd = spark.sparkContext.parallelize(data)
        schema = ["time", "altitude", "latitude", "longitude", "fluorescence"]
        df = spark.createDataFrame(rdd, schema=schema)

        # Data transformations
        df_clean = df.withColumn("time", to_timestamp("time")) \
                     .withColumn("fluorescence", col("fluorescence").cast("float")) \
                     .filter(col("latitude").isNotNull() & col("longitude").isNotNull())

        # Write transformed data to HDFS
        write_to_hdfs(df_clean, hdfs_path)
        spark_logger.info("PMN data transformation and caching successful.")
        return df_clean.collect()

    except Exception as e:
        spark_logger.error(f"Error processing PMN data: {str(e)}")
        raise GraphQLError("Error fetching or transforming PMN data.")


def fetch_and_transform_buoy_data(url):
    """
    Fetch and transform buoy data using Spark and store results in HDFS.
    """
    spark = create_spark_session()
    hdfs_path = "/data/buoy_data.parquet"  # HDFS path for cached buoy data

    try:
        # Check if data is already cached in HDFS
        if hdfs_file_exists(spark, hdfs_path):
            spark_logger.info("Buoy data found in HDFS. Loading from cache.")
            df_cached = spark.read.parquet(hdfs_path)
            return df_cached.collect()

        # Fetch buoy data from the API
        response = requests.get(url)
        if response.status_code != 200:
            raise GraphQLError(f"Failed to fetch buoy data: {response.status_code}")

        # Split API response into lines and parse data
        lines = response.text.splitlines()[2:]  # Skip header lines
        if not lines:
            raise GraphQLError("No buoy data available for the given station.")

        rdd = spark.sparkContext.parallelize([line.split() for line in lines])
        schema = ["year", "month", "day", "hour", "minute", "wave_height", "sst", "station"]
        df = spark.createDataFrame(rdd, schema=schema)

        # Data transformations
        df_clean = df.withColumn(
            "timestamp",
            to_timestamp(concat_ws(" ", "year", "month", "day", "hour", "minute"), "yyyy MM dd HH mm")
        ).withColumn("wave_height", col("wave_height").cast("float")) \
         .withColumn("sst", col("sst").cast("float")) \
         .filter(col("wave_height").isNotNull())

        # Write transformed data to HDFS
        write_to_hdfs(df_clean, hdfs_path)
        spark_logger.info("Buoy data transformation and caching successful.")
        return df_clean.collect()

    except Exception as e:
        spark_logger.error(f"Error processing buoy data: {str(e)}")
        raise GraphQLError("Error fetching or transforming buoy data.")

def fetch_and_transform_climate_data(dataset_id, location_id, start_date, end_date):
    spark = create_spark_session()
    headers = {"token": NOAA_TOKEN}
    
    # Convert DateTime inputs to strings in ISO format
    start_date_str = start_date.isoformat() if isinstance(start_date, datetime) else start_date
    end_date_str = end_date.isoformat() if isinstance(end_date, datetime) else end_date

    url = (
        f"https://www.ncdc.noaa.gov/cdo-web/api/v2/data?"
        f"datasetid={dataset_id}&locationid={location_id}&datatypeid=AWND,WDF2,WSF2"
        f"&startdate={start_date_str}&enddate={end_date_str}&limit=1000"
    )

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise GraphQLError(f"Failed to fetch climate data: {response.status_code}")

        data = response.json().get("results", [])
        filtered_data = [item for item in data if item["datatype"] in {"AWND", "WDF2", "WSF2"}]

        spark_logger.info(f"Fetched {len(filtered_data)} climate records.")
        return [
            ClimateData(
                date=item["date"],
                datatype=item["datatype"],
                value=item["value"],
                station=item.get("station", ""),
                attributes=item.get("attributes", "")
            )
            for item in filtered_data
        ]
    except Exception as e:
        spark_logger.error(f"Error processing climate data: {str(e)}")
        raise GraphQLError("Error fetching or transforming climate data.")


# GraphQL Schema and Route Setup
schema = graphene.Schema(query=Query)
app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True))

# Run Flask server
if __name__ == "__main__":
    try:
        print("Starting Flask server...")
        app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
        print("Flask server has started.")
    except OSError as e:
        print(f"Error: {e}")