import json
from kafka import KafkaConsumer
from ingestion.logger import logger
from ingestion.config import KafkaConfig
from ingestion.dlq_handler import send_to_dlq
from typing import Callable, Dict


class KafkaConsumerManager:
    """
    Manages Kafka consumer operations, including message processing and error handling.
    """

    def __init__(self, topic_key: str, message_handler: Callable[[Dict], None]):
        """
        Initializes the KafkaConsumerManager and creates a Kafka consumer instance.

        Args:
            topic_key (str): The key for the Kafka topic in KafkaConfig.TOPICS.
            message_handler (Callable[[Dict], None]): Function to handle incoming messages.

        Raises:
            ValueError: If the topic key is invalid.
        """
        if topic_key not in KafkaConfig.TOPICS:
            raise ValueError(f"Topic '{topic_key}' not found in KafkaConfig.TOPICS")

        self.topic = KafkaConfig.TOPICS[topic_key]
        self.consumer = self._create_consumer()
        self.message_handler = message_handler

    def _create_consumer(self) -> KafkaConsumer:
        """
        Creates and returns a Kafka consumer instance.

        Returns:
            KafkaConsumer: The Kafka consumer instance.
        """
        try:
            consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=KafkaConfig.BOOTSTRAP_SERVERS,
                auto_offset_reset="latest",
                enable_auto_commit=True,
                group_id=KafkaConfig.GROUP_ID,
                value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            )
            logger.info("Kafka consumer created for topic '%s'.", self.topic)
            return consumer
        except Exception as e:
            logger.error("Failed to create Kafka consumer: %s", e)
            raise

    def consume_messages(self):
        """
        Consumes messages from the Kafka topic and processes them using the provided message handler.
        """
        try:
            for message in self.consumer:
                logger.info("Message received: %s", message.value)
                try:
                    self.message_handler(message.value)
                except Exception as e:
                    logger.error("Message processing failed: %s", e)
                    send_to_dlq(KafkaProducerManager(), KafkaConfig.TOPICS["dlq"], message.value)
        except Exception as e:
            logger.error("Error while consuming messages: %s", e)
            raise

    def close(self):
        """
        Closes the Kafka consumer.
        """
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer closed.")


if __name__ == "__main__":
    # Example message handler
    def example_handler(message: Dict):
        logger.info("Processing message: %s", message)

    consumer_manager = KafkaConsumerManager(topic_key="main", message_handler=example_handler)

    try:
        consumer_manager.consume_messages()
    except KeyboardInterrupt:
        logger.info("Consumer interrupted by user.")
    finally:
        consumer_manager.close()