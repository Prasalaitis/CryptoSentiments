import json
from kafka import KafkaProducer
from ingestion.logger import logger
from ingestion.config import KAFKA_BOOTSTRAP_SERVERS


def create_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
            retries=5,
        )
        logger.info("Kafka producer created.")
        return producer
    except Exception as e:
        logger.error("Failed to create Kafka producer: %s", e)
        raise


def send_message(producer, topic, message):
    try:
        producer.send(topic, value=message).get(timeout=10)
        logger.info("Message sent to topic '%s': %s", topic, message)
    except Exception as e:
        logger.error("Failed to send message to Kafka: %s", e)
