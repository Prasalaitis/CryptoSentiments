from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
    kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    kafka_topic = os.getenv("KAFKA_TOPIC", "reddit_data")
    output_format = os.getenv("OUTPUT_FORMAT", "console")  # Options: console, parquet, etc.
    output_path = os.getenv("OUTPUT_PATH", "/tmp/output")  # Path for file-based output

    # Initialize Spark session
    spark = SparkSession.builder.appName("RedditStream").getOrCreate()

    try:
        # Read data from Kafka
        logging.info("Reading data from Kafka topic: %s", kafka_topic)
        df = spark.readStream.format("kafka") \
            .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
            .option("subscribe", kafka_topic) \
            .option("startingOffsets", "latest") \
            .load()

        # Select and process the value column
        df = df.selectExpr("CAST(value AS STRING) as text")

        # Add sentiment analysis column
        processed_df = df.withColumn("sentiment", analyze_sentiment_udf(col("text")))

        # Write the processed stream to the output destination
        logging.info("Writing the processed stream to the %s output...", output_format)
        if output_format == "console":
            query = processed_df.writeStream.format("console").outputMode("append").start()
        elif output_format == "parquet":
            query = processed_df.writeStream.format("parquet") \
                .option("path", output_path) \
                .option("checkpointLocation", f"{output_path}/checkpoints") \
                .outputMode("append").start()
        else:
            logging.error("Unsupported output format: %s", output_format)
            return

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
