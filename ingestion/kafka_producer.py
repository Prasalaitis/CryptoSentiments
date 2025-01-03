import json
from kafka import KafkaProducer
from ingestion.logger import logger
from ingestion.config import KAFKA_BOOTSTRAP_SERVERS

class KafkaProducerManager:
    def __init__(self):
        """
        Initializes the KafkaProducerManager and creates a Kafka producer instance.
        """
        self.bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS
        self.producer = self._create_producer()

    def _create_producer(self):
        """
        Creates and returns a Kafka producer instance.
        """
        try:
            producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda x: json.dumps(x).encode("utf-8"),
                retries=5,
            )
            logger.info("Kafka producer created.")
            return producer
        except Exception as e:
            logger.error("Failed to create Kafka producer: %s", e)
            raise

    def send_message(self, topic, message):
        """
        Sends a message to a Kafka topic.

        Args:
            topic (str): The Kafka topic to send the message to.
            message (dict): The message to send.
        """
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
