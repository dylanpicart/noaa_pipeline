def get_yarn_spark_config():
    return {
        "spark.master": "yarn",
        "spark.hadoop.fs.defaultFS": "hdfs://namenode:9000",
        "spark.dynamicAllocation.enabled": "true",
        "spark.executor.memory": "2g",
        "spark.executor.cores": "2",
        "spark.executor.instances": "4",
        "spark.yarn.queue": "default",
        "spark.yarn.am.memory": "1g",
        "spark.executor.memoryOverhead": "512m"
    }
