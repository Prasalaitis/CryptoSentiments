import os
from dotenv import load_dotenv
from typing import Dict

# Load environment variables from a .env file if it exists
load_dotenv()

class KafkaConfig:
    """
    A class to encapsulate Kafka configurations for better reusability.
    """
    # Kafka Connection
    BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    PARTITIONS: int = int(os.getenv("KAFKA_PARTITIONS", 3))
    REPLICATION_FACTOR: int = int(os.getenv("KAFKA_REPLICATION_FACTOR", 2))
    GROUP_ID: str = os.getenv("KAFKA_GROUP_ID", "default-consumer-group")

    # Kafka Topics
    TOPICS: Dict[str, str] = {
        "main": os.getenv("KAFKA_MAIN_TOPIC", "cryptocurrency_events"),
        "results": os.getenv("KAFKA_RESULTS_TOPIC", "sentiment_analysis_results"),
        "dlq": os.getenv("KAFKA_DLQ_TOPIC", "dead_letter_queue"),
    }

    @property
    def DLQ_TOPIC(self) -> str:
        """Returns the Dead Letter Queue topic."""
        return self.TOPICS["dlq"]

    @staticmethod
    def validate():
        """
        Validates critical Kafka configurations.
        Raises:
            ValueError: If a required configuration is missing.
        """
        if not KafkaConfig.BOOTSTRAP_SERVERS:
            raise ValueError("KAFKA_BOOTSTRAP_SERVERS is not set!")

        if not KafkaConfig.TOPICS["main"]:
            raise ValueError("KAFKA_MAIN_TOPIC is not set!")

        if not KafkaConfig.TOPICS["dlq"]:
            raise ValueError("KAFKA_DLQ_TOPIC is not set!")

# Validate configurations at runtime
KafkaConfig.validate()
