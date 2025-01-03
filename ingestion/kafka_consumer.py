import json
from kafka import KafkaConsumer
from ingestion.logger import logger
from ingestion.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID, DLQ_TOPIC
from ingestion.dlq_handler import send_to_dlq


class KafkaConsumerManager:
    def __init__(self, topic):
        """
        Initializes the KafkaConsumerManager and creates a Kafka consumer instance for the given topic.

        Args:
            topic (str): The Kafka topic to subscribe to.
        """
        self.topic = topic
        self.consumer = self._create_consumer()

    def _create_consumer(self):
        """
        Creates and returns a Kafka consumer instance.
        """
        try:
            consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                auto_offset_reset="latest",
                enable_auto_commit=True,
                group_id=KAFKA_GROUP_ID,
                value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            )
            logger.info("Kafka consumer created for topic '%s'.", self.topic)
            return consumer
        except Exception as e:
            logger.error("Failed to create Kafka consumer: %s", e)
            raise

    def process_message(self, message, producer):
        """
        Processes a single Kafka message.

        Args:
            message (dict): The Kafka message to process.
            producer: Kafka producer instance for sending messages to the DLQ.
        """
        try:
            if "error" in message:
                raise ValueError("Processing error!")
            logger.info("Message processed successfully: %s", message)
        except Exception as e:
            logger.error("Message processing failed: %s", e)
            send_to_dlq(producer, DLQ_TOPIC, message)

    def consume_messages(self, producer):
        """
        Consumes messages from the Kafka topic and processes them.

        Args:
            producer: Kafka producer instance for sending messages to the DLQ.
        """
        try:
            for message in self.consumer:
                logger.info("Message received: %s", message.value)
                self.process_message(message.value, producer)
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
