from ingestion.kafka_producer import KafkaProducerManager
from ingestion.logger import logger
from typing import Dict


def send_to_dlq(producer_manager: KafkaProducerManager, topic: str, message: Dict) -> None:
    """
    Sends a failed message to the Dead Letter Queue (DLQ).

    Args:
        producer_manager (KafkaProducerManager): Kafka producer manager instance.
        topic (str): Kafka topic name for DLQ.
        message (Dict): The message to send to DLQ.

    Raises:
        ValueError: If the message or topic is invalid.
    """
    if not topic:
        raise ValueError("DLQ topic cannot be empty.")
    if not isinstance(message, dict):
        raise ValueError("Message must be a dictionary.")

    try:
        logger.info("Sending message to DLQ topic '%s': %s", topic, message)
        producer_manager.send_message(topic, message)
        logger.info("Message successfully sent to DLQ.")
    except Exception as e:
        logger.error("Failed to send message to DLQ: %s", e)
        logger.debug("Message details: %s", message)


def retry_failed_message(
    producer_manager: KafkaProducerManager, topic: str, message: Dict, max_retries: int = 3
) -> None:
    """
    Retries sending a failed message to the DLQ with a limited number of attempts.

    Args:
        producer_manager (KafkaProducerManager): Kafka producer manager instance.
        topic (str): Kafka topic name for DLQ.
        message (Dict): The message to send to DLQ.
        max_retries (int): Maximum number of retries before giving up.

    Raises:
        ValueError: If the message or topic is invalid.
    """
    retries = 0
    while retries < max_retries:
        try:
            send_to_dlq(producer_manager, topic, message)
            return
        except Exception as e:
            retries += 1
            logger.warning(
                "Retry %d/%d failed for message to topic '%s': %s",
                retries,
                max_retries,
                topic,
                e,
            )

    logger.error(
        "Failed to send message to DLQ after %d retries. Message dropped: %s", max_retries, message
    )
