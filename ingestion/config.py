import os

# Kafka configurations
KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
)
KAFKA_TOPICS = os.getenv(
    "KAFKA_TOPICS", "reddit_data,dead_letter_queue"
).split(",")
KAFKA_PARTITIONS = int(os.getenv("KAFKA_PARTITIONS", 3))
KAFKA_REPLICATION_FACTOR = int(os.getenv("KAFKA_REPLICATION_FACTOR", 1))
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "meme-coin-consumer-group")
DLQ_TOPIC = os.getenv("DLQ_TOPIC", "dead_letter_queue")
