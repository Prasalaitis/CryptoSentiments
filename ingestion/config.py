import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_PARTITIONS = int(os.getenv("KAFKA_PARTITIONS", 3))
KAFKA_REPLICATION_FACTOR = int(os.getenv("KAFKA_REPLICATION_FACTOR", 2))
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "default-consumer-group")

# Topics Configuration
KAFKA_TOPICS = {
    "main": os.getenv("KAFKA_MAIN_TOPIC", "cryptocurrency_events"),
    "results": os.getenv("KAFKA_RESULTS_TOPIC", "sentiment_analysis_results"),
    "dlq": os.getenv("KAFKA_DLQ_TOPIC", "dead_letter_queue"),
}

# Dead Letter Queue (DLQ) Topic
DLQ_TOPIC = KAFKA_TOPICS["dlq"]

# Validation for critical configurations
if not KAFKA_BOOTSTRAP_SERVERS:
    raise ValueError("KAFKA_BOOTSTRAP_SERVERS environment variable is not set!")

if not KAFKA_TOPICS["main"]:
    raise ValueError("KAFKA_MAIN_TOPIC environment variable is not set!")

if not KAFKA_TOPICS["dlq"]:
    raise ValueError("KAFKA_DLQ_TOPIC environment variable is not set!")
