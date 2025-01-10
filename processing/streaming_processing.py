from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, from_json
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
import logging
import os
from ingestion.dlq_handler import send_to_dlq

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Placeholder sentiment analysis function
def analyze_sentiment(text: str) -> str:
    """
    Analyze the sentiment of a given text.
    Replace this placeholder with an actual sentiment analysis model.
    """
    # Example logic: Replace with actual NLP model integration
    if "good" in text.lower():
        return "positive"
    elif "bad" in text.lower():
        return "negative"
    else:
        return "neutral"

# Register the UDF for sentiment analysis
analyze_sentiment_udf = udf(analyze_sentiment, StringType())

def main():
    # Load configurations
    kafka_bootstrap_servers = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
    )
    kafka_topic = os.getenv("KAFKA_TOPIC", "cryptocurrency_events")
    output_topic = os.getenv("OUTPUT_TOPIC", "sentiment_analysis_results")

    # Define the schema for incoming data
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("subreddit", StringType(), True),
        StructField("title", StringType(), True),
        StructField("body", StringType(), True),
        StructField("timestamp", TimestampType(), True),
    ])

    # Initialize Spark session
    spark = SparkSession.builder.appName("RedditStreamProcessor").getOrCreate()

    try:
        # Read data from Kafka
        logging.info("Reading data from Kafka topic: %s", kafka_topic)
        df = (
            spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
            .option("subscribe", kafka_topic)
            .option("startingOffsets", "latest")
            .load()
        )

        # Deserialize and apply schema
        df = df.selectExpr("CAST(value AS STRING) as json")
        parsed_df = df.select(from_json(col("json"), schema).alias("data")).select("data.*")

        # Add sentiment analysis column
        processed_df = parsed_df.withColumn(
            "sentiment", analyze_sentiment_udf(col("body"))
        )

        # Write the processed stream back to Kafka
        logging.info("Writing the processed stream to Kafka topic: %s", output_topic)
        query = (
            processed_df.selectExpr("to_json(struct(*)) AS value")
            .writeStream
            .format("kafka")
            .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
            .option("topic", output_topic)
            .outputMode("append")
            .start()
        )

        # Await termination
        query.awaitTermination()

    except Exception as e:
        logging.error("An error occurred: %s", e)
    finally:
        # Stop the Spark session gracefully
        logging.info("Stopping Spark session...")
        spark.stop()

if __name__ == "__main__":
    main()
