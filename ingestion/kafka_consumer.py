import json
from kafka import KafkaConsumer
from ingestion.logger import logger
from ingestion.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID, DLQ_TOPIC
from ingestion.dlq_handler import send_to_dlq


def create_consumer(topic):
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset="latest",
            enable_auto_commit=True,
            group_id=KAFKA_GROUP_ID,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )
        logger.info("Kafka consumer created for topic '%s'.", topic)
        return consumer
    except Exception as e:
        logger.error("Failed to create Kafka consumer: %s", e)
        raise


def process_message(message, producer):
    try:
        if "error" in message:
            raise ValueError("Processing error!")
        logger.info("Message processed successfully: %s", message)
    except Exception as e:
        logger.error("Message processing failed: %s", e)
        send_to_dlq(producer, DLQ_TOPIC, message)
