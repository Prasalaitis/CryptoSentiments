import json
from kafka import KafkaProducer
from ingestion.logger import logger
from ingestion.config import KafkaConfig


class KafkaProducerManager:
    """
    A class to manage Kafka producer operations.
    """

    def __init__(self):
        """
        Initializes the KafkaProducerManager and creates a Kafka producer instance.
        """
        self.producer = self._create_producer()

    def _create_producer(self):
        """
        Creates and returns a Kafka producer instance.
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

    def send_message(self, topic_key, message):
        """
        Sends a message to a Kafka topic.

        Args:
            topic_key (str): The key for the Kafka topic in KafkaConfig.TOPICS.
            message (dict): The message to send.
        """
        if topic_key not in KafkaConfig.TOPICS:
            raise ValueError(f"Topic '{topic_key}' not found in KafkaConfig.TOPICS")

        topic = KafkaConfig.TOPICS[topic_key]
        try:
            self.producer.send(topic, value=message).get(timeout=10)
            logger.info("Message sent to topic '%s': %s", topic, message)
        except Exception as e:
            logger.error("Failed to send message to Kafka: %s", e)
            raise

    def close(self):
        """
        Closes the Kafka producer.
        """
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed.")
