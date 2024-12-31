from kafka_producer import create_producer, send_message
from logger import logger

def send_to_dlq(producer, topic, message):
    """
    Sends a failed message to the Dead Letter Queue (DLQ).
    """
    try:
        send_message(producer, topic, message)
        logger.info("Message sent to DLQ: %s", message)
    except Exception as e:
        logger.error("Failed to send message to DLQ: %s", e)
