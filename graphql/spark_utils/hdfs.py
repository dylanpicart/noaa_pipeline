from py4j.protocol import Py4JJavaError

def hdfs_file_exists(spark, path):
    try:
        hadoop_conf = spark._jsc.hadoopConfiguration()
        fs = spark._jvm.org.apache.hadoop.fs.FileSystem.get(hadoop_conf)
        return fs.exists(spark._jvm.org.apache.hadoop.fs.Path(path))
    except Py4JJavaError:
        return False

def write_to_hdfs(df, path):
    df.write.mode("overwrite").parquet(path)
