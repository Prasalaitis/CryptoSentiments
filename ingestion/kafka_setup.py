from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError, TopicAlreadyExistsError
from ingestion.config import KafkaConfig
from ingestion.logger import logger
from typing import List


class KafkaTopicManager:
    """
    Manages Kafka topics, including creation and validation.
    """

    def __init__(self):
        """
        Initializes the KafkaTopicManager with Kafka Admin Client.
        """
        try:
            self.admin_client = KafkaAdminClient(
                bootstrap_servers=KafkaConfig.BOOTSTRAP_SERVERS,
                client_id="admin",
            )
            logger.info("Kafka Admin Client initialized.")
        except KafkaError as e:
            logger.error("Failed to initialize Kafka Admin Client: %s", e)
            raise

    def list_existing_topics(self) -> List[str]:
        """
        Retrieves the list of existing Kafka topics.

        Returns:
            List[str]: A list of existing Kafka topic names.
        """
        try:
            existing_topics = list(self.admin_client.list_topics())
            logger.info("Existing topics: %s", existing_topics)
            return existing_topics
        except KafkaError as e:
            logger.error("Failed to fetch existing topics: %s", e)
            raise

    def create_topics(self, topics: List[str]) -> List[str]:
        """
        Creates Kafka topics if they don't already exist.

        Args:
            topics (List[str]): List of topic names to create.

        Returns:
            List[str]: List of newly created topics.
        """
        try:
            existing_topics = set(self.list_existing_topics())
            new_topics = [
                NewTopic(
                    name=topic,
                    num_partitions=KafkaConfig.PARTITIONS,
                    replication_factor=KafkaConfig.REPLICATION_FACTOR,
                )
                for topic in topics if topic not in existing_topics
            ]

            if new_topics:
                self.admin_client.create_topics(new_topics=new_topics, validate_only=False)
                created_topics = [topic.name for topic in new_topics]
                logger.info("Created topics: %s", created_topics)
                return created_topics

            logger.info("No new topics to create. All topics already exist.")
            return []

        except TopicAlreadyExistsError as e:
            logger.warning("Some topics already exist: %s", e)
            return []
        except KafkaError as e:
            logger.error("Kafka error occurred while creating topics: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error during topic creation: %s", e)
            raise

    def close(self) -> None:
        """
        Closes the Kafka Admin Client.
        """
        if self.admin_client:
            self.admin_client.close()
            logger.info("Kafka Admin Client closed.")


if __name__ == "__main__":
    topic_manager = KafkaTopicManager()

    try:
        topics_to_create = list(KafkaConfig.TOPICS.values())
        new_topics = topic_manager.create_topics(topics_to_create)

        if new_topics:
            logger.info("Successfully created topics: %s", new_topics)
        else:
            logger.info("No new topics were created.")
    except Exception as e:
        logger.error("Error in Kafka topic management: %s", e)
    finally:
        topic_manager.close()