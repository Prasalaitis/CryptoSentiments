from ingestion.kafka_producer import send_message
from ingestion.logger import logger


def send_to_dlq(producer, topic, message):
    """
    Sends a failed message to the Dead Letter Queue (DLQ).

    Args:
        producer: Kafka producer instance.
        topic (str): Kafka topic name for DLQ.
        message (dict): The message to send to DLQ.
    """
    try:
        send_message(producer, topic, message)
        logger.info("Message sent to DLQ: %s", message)
    except Exception as e:
        logger.error("Failed to send message to DLQ: %s", e)
