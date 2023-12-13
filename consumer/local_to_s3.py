import pyspark
from delta import *
from pyspark.sql.functions import year, month
import configparser, logging as log, os

packages = [
    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1",
    "io.delta:delta-spark_2.12:3.0.0,org.apache.hadoop:hadoop-aws:3.3.1",
]

config_ini_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "producer")
config = configparser.ConfigParser(); config.read(f"{config_ini_path}/.ini")
log.basicConfig(level=log.INFO)

builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.hadoop.fs.s3a.access.key", config['AWS']['aws_access_key']) \
    .config("spark.hadoop.fs.s3a.secret.key", config['AWS']['aws_secret_key']) \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") 

spark = configure_spark_with_delta_pip(builder, extra_packages=packages).getOrCreate()


df = spark.read.format("delta").load(config['DEFAULT']['delta_lake_path'])
df.show()
df.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("year", "month") \
    .option("maxRecordsPerFile", "10000") \
    .save(config['AWS']['s3_bucket_path'])