from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, from_json
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Placeholder sentiment analysis function
def analyze_sentiment(text: str) -> str:
    if "good" in text.lower():
        return "positive"
    elif "bad" in text.lower():
        return "negative"
    else:
        return "neutral"

# Register the UDF for sentiment analysis
analyze_sentiment_udf = udf(analyze_sentiment, StringType())

def write_to_snowflake(processed_df):
    # Snowflake connection options
    snowflake_options = {
        "sfURL": os.getenv("SNOWFLAKE_ACCOUNT") + ".snowflakecomputing.com",
        "sfDatabase": os.getenv("SNOWFLAKE_DATABASE"),
        "sfSchema": os.getenv("SNOWFLAKE_SCHEMA"),
        "sfWarehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "sfRole": os.getenv("SNOWFLAKE_ROLE"),
        "sfUser": os.getenv("SNOWFLAKE_USER"),
        "sfPassword": os.getenv("SNOWFLAKE_PASSWORD"),
    }

    logging.info("Writing processed data to Snowflake...")

    # Write processed data to Snowflake
    processed_df.writeStream \
        .format("net.snowflake.spark.snowflake") \
        .options(**snowflake_options) \
        .option("dbtable", "sentiment_analysis_results") \
        .outputMode("append") \
        .start()

def main():
    # Load configurations
    kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    kafka_topic = os.getenv("KAFKA_TOPIC", "cryptocurrency_events")
    output_topic = os.getenv("OUTPUT_TOPIC", "sentiment_analysis_results")
    s3_raw_data_path = os.getenv("S3_RAW_DATA_PATH", "s3a://your-bucket-name/raw-data/")
    checkpoint_location = os.getenv("CHECKPOINT_LOCATION", "s3a://your-bucket-name/checkpoints/")

    # Define schema for incoming data
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("subreddit", StringType(), True),
        StructField("title", StringType(), True),
        StructField("body", StringType(), True),
        StructField("timestamp", TimestampType(), True),
    ])

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("RedditStreamProcessor") \
        .config("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID")) \
        .config("spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY")) \
        .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
        .getOrCreate()

    try:
        # Read raw data from Kafka
        logging.info("Reading data from Kafka topic: %s", kafka_topic)
        raw_df = spark.readStream.format("kafka") \
            .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
            .option("subscribe", kafka_topic) \
            .option("startingOffsets", "latest") \
            .load()

        # Deserialize and apply schema
        raw_parsed_df = raw_df.selectExpr("CAST(value AS STRING) as json") \
            .select(from_json(col("json"), schema).alias("data")) \
            .select("data.*")

        # Save raw data to S3
        logging.info("Writing raw data to S3: %s", s3_raw_data_path)
        raw_query = raw_parsed_df.writeStream \
            .format("json") \
            .option("path", s3_raw_data_path) \
            .option("checkpointLocation", os.path.join(checkpoint_location, "raw-data")) \
            .outputMode("append") \
            .start()

        # Process data with sentiment analysis
        processed_df = raw_parsed_df.withColumn(
            "sentiment", analyze_sentiment_udf(col("body"))
        )

        # Write processed data to Kafka
        logging.info("Writing processed data to Kafka topic: %s", output_topic)
        processed_query = processed_df.selectExpr("to_json(struct(*)) AS value") \
            .writeStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
            .option("topic", output_topic) \
            .option("checkpointLocation", os.path.join(checkpoint_location, "processed-data")) \
            .outputMode("append") \
            .start()

        # Write processed data to Snowflake
        write_to_snowflake(processed_df)

        # Await termination
        raw_query.awaitTermination()
        processed_query.awaitTermination()

    except Exception as e:
        logging.error("An error occurred: %s", e)
    finally:
        logging.info("Stopping Spark session...")
        spark.stop()

if __name__ == "__main__":
    main()
