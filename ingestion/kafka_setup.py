from kafka.admin import KafkaAdminClient, NewTopic
from ingestion.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPICS,
    KAFKA_PARTITIONS,
    KAFKA_REPLICATION_FACTOR,
)
from ingestion.logger import logger


def create_topics(topics):
    """
    Creates Kafka topics if they don't already exist.

    Args:
        topics (list): List of topic names to create.
    """
    try:
        # Initialize Kafka Admin Client
        admin_client = KafkaAdminClient(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, client_id="admin"
        )

        # Prepare topics to be created
        new_topics = [
            NewTopic(
                name=topic,
                num_partitions=KAFKA_PARTITIONS,
                replication_factor=KAFKA_REPLICATION_FACTOR,
            )
            for topic in topics
        ]

        # Create topics
        admin_client.create_topics(new_topics=new_topics, validate_only=False)
        logger.info("Created topics: %s", topics)
    except Exception as e:
        logger.error("Failed to create topics: %s", e)
        raise


if __name__ == "__main__":
    # Create topics defined in config.py
    create_topics(KAFKA_TOPICS)
