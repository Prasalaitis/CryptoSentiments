import os
import logging
from kafka import KafkaConsumer
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load Kafka configurations
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "reddit_data")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "meme-coin-consumer-group")

def create_consumer():
    """
    Creates a Kafka consumer for JSON deserialization.
    """
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id=KAFKA_GROUP_ID,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )
    logging.info("Kafka consumer created successfully.")
    return consumer

if __name__ == "__main__":
    consumer = create_consumer()
    for message in consumer:
        logging.info("Received message: %s", message.value)
