import pyspark
from delta import *
from pyspark.sql.functions import year, month
import configparser, logging as log, os

packages = [
    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1"
]

builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") 

spark = configure_spark_with_delta_pip(builder, extra_packages=packages).getOrCreate()

config_ini_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "producer")
config = configparser.ConfigParser(); config.read(f"{config_ini_path}/.ini")
log.basicConfig(level=log.INFO)

kafka_params = {
    "kafka.bootstrap.servers": config['DEFAULT']['bootstrap_servers'],
    "subscribe": "test_order-placement, test_shipment-tracking, test_validate-shipment-tracking, test_KPI-analytics",
    "startingOffsets": "earliest" 
}

#spark.read.format("delta").load("s3a://my-aws-pyspark-table/test").show()

kafka_source = spark \
    .readStream \
    .format("kafka") \
    .options(**kafka_params) \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load()

df = kafka_source.selectExpr("CAST(value AS STRING)", "CAST(key AS STRING)", "topic", "offset","timestamp")
month_data = df.withColumn("month", month("timestamp")); 
month_year_data = month_data.withColumn("year", year("timestamp"))



query = month_year_data \
    .writeStream \
    .outputMode("append") \
    .format("delta") \
    .partitionBy("year", "month") \
    .option("path", config['DEFAULT']['delta_lake_path']) \
    .option("checkpointLocation", config['DEFAULT']['checkpointLocation']) \
    .option("maxRecordsPerFile", "10000") \
    .start()

# Await termination of the streaming query
query.awaitTermination()