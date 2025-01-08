import json
from kafka import KafkaProducer
from ingestion.logger import logger
from ingestion.config import KafkaConfig
from typing import Dict


class KafkaProducerManager:
    """
    A class to manage Kafka producer operations, including message serialization and retries.
    """

    def __init__(self):
        """
        Initializes the KafkaProducerManager and creates a Kafka producer instance.
        """
        self.producer = self._create_producer()

    def _create_producer(self) -> KafkaProducer:
        """
        Creates and returns a Kafka producer instance.

        Returns:
            KafkaProducer: The Kafka producer instance.
        """
        try:
            producer = KafkaProducer(
                bootstrap_servers=KafkaConfig.BOOTSTRAP_SERVERS,
                value_serializer=lambda x: json.dumps(x).encode("utf-8"),
                retries=5,
            )
            logger.info("Kafka producer created.")
            return producer
        except Exception as e:
            logger.error("Failed to create Kafka producer: %s", e)
            raise

    def send_message(self, topic_key: str, message: Dict, retries: int = 3) -> None:
        """
        Sends a message to a Kafka topic with retry logic.

        Args:
            topic_key (str): The key for the Kafka topic in KafkaConfig.TOPICS.
            message (Dict): The message to send.
            retries (int): Number of retries for sending the message.

        Raises:
            ValueError: If the topic key is invalid.
        """
        if topic_key not in KafkaConfig.TOPICS:
            raise ValueError(f"Topic '{topic_key}' not found in KafkaConfig.TOPICS")

        topic = KafkaConfig.TOPICS[topic_key]
        attempt = 0

        while attempt <= retries:
            try:
                logger.info("Sending message to topic '%s': %s", topic, message)
                self.producer.send(topic, value=message).get(timeout=10)
                logger.info("Message successfully sent to topic '%s'.", topic)
                return
            except Exception as e:
                attempt += 1
                logger.warning(
                    "Attempt %d/%d failed for topic '%s': %s",
                    attempt,
                    retries,
                    topic,
                    e,
                )

        logger.error("Failed to send message to topic '%s' after %d retries. Message dropped.", topic, retries)

    def close(self) -> None:
        """
        Closes the Kafka producer.
        """
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed.")


if __name__ == "__main__":
    producer_manager = KafkaProducerManager()

    try:
        sample_message = {"key": "value"}
        producer_manager.send_message(topic_key="main", message=sample_message)
    except Exception as e:
        logger.error("Error in Kafka producer: %s", e)
    finally:
        producer_manager.close()