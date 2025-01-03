from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError, TopicAlreadyExistsError
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

    Returns:
        list: List of newly created topics.
    """
    try:
        # Initialize Kafka Admin Client
        with KafkaAdminClient(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, client_id="admin"
        ) as admin_client:
            # Fetch existing topics
            existing_topics = set(admin_client.list_topics())
            logger.info("Existing topics: %s", existing_topics)

            # Filter out topics that already exist
            new_topics = [
                NewTopic(
                    name=topic,
                    num_partitions=KAFKA_PARTITIONS,
                    replication_factor=KAFKA_REPLICATION_FACTOR,
                )
                for topic in topics if topic not in existing_topics
            ]

            if new_topics:
                # Create new topics
                admin_client.create_topics(new_topics=new_topics, validate_only=False)
                logger.info("Created topics: %s", [topic.name for topic in new_topics])
                return [topic.name for topic in new_topics]
            else:
                logger.info("No new topics to create. All topics already exist.")
                return []
    except TopicAlreadyExistsError as e:
        logger.warning("Some topics already exist: %s", e)
        return []
    except KafkaError as e:
        logger.error("Kafka error occurred: %s", e)
        raise
    except Exception as e:
        logger.error("Failed to create topics: %s", e)
        raise


if __name__ == "__main__":
    # Extract topic names from config and create them
    new_topics = create_topics(list(KAFKA_TOPICS.values()))
    if new_topics:
        logger.info("Successfully created topics: %s", new_topics)
    else:
        logger.info("No topics were created.")
